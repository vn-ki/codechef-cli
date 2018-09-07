import random
import string
import requests
from flask import Flask, request
import webbrowser

class Codechef:
    """Codechef API
        call `start_oauth_flow` to start the flow
    """
    app = Flask(__name__)
    def __init__(self, client_id, client_secret, redirect_uri='http://127.0.0.1:8080/callback'):
        self.client_id = client_id;
        self.client_secret = client_secret;
        self.redirect_uri = redirect_uri;
        self.app.route("/callback")(self.recieve_tokens)
        
    def start_oauth_flow(self):
        redir_url = self.get_oauth_url()
        webbrowser.open(redir_url)
        self.app.run(port=8080,host='0.0.0.0')

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        
    def recieve_tokens(self):
        #request.args['code'] is what we need
        self.shutdown_server()
        try:
            code = request.args['code']
            r = requests.post("https://api.codechef.com/oauth/token", 
                    json={
                        "grant_type": "authorization_code",
                        "code": code,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uri": self.redirect_uri,
                    },
                    headers={'content-Type': 'application/json'})
            response = r.json()
            self.tokens = response['result']['data'];
        #TODO: handle exceptions carefully
        except Exception:
            pass
        return "You can close this tab."
    
    def get_oauth_url(self):
        return f"https://api.codechef.com/oauth/authorize?\
                    response_type=code&\
                    client_id={self.client_id}&\
                    redirect_uri={self.redirect_uri}&\
                    state={self.get_random_state()}"

    # maybe add some more security using `state` params
    def get_random_state(self):
        return ''.join(random.choices(string.ascii_letters,k=9))
