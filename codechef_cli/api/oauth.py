import random
import string
import requests
import webbrowser
import logging
from flask import Flask, request

logger = logging.Logger(__name__)
#set werkzeug's logging to ERROR only
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

class CodechefOauth:
    """Codechef API
        call `start_oauth_flow` to start the flow
    """
    app = Flask(__name__)
    def __init__(self, client_id, client_secret, redirect_uri='http://127.0.0.1:8080/callback'):
        self.client_id = client_id;
        self.client_secret = client_secret;
        self.redirect_uri = redirect_uri;
        self.app.route("/callback")(self._recieve_tokens)
        
    def start_oauth_flow(self):
        """starts the oauth flow"""
        #TODO:find a way to hide flask's 'server started' info
        redir_url = self.get_oauth_url()
        webbrowser.open(redir_url)
        self.app.run(port=8080,host='0.0.0.0')
        logger.debug("Server has started")

    def get_oauth_url(self):
        return f"https://api.codechef.com/oauth/authorize?\
                    response_type=code&\
                    client_id={self.client_id}&\
                    redirect_uri={self.redirect_uri}&\
                    state={self._get_random_state()}"

    def _shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        
    def _recieve_tokens(self):
        """called when user visits /callback """
        self._shutdown_server()
        logger.debug("user visited /callback, args:",request.args)
        try:
            code = request.args['code']
            #exchange code for tokens
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
            logger.debug("Response from codechef:",response)
            self.tokens = response['result']['data'];
        #TODO: handle exceptions carefully
        except Exception:
            pass
        return "You can close this tab."
    
    def _get_random_state(self):
        """generates a random string of length 9"""
        return ''.join(random.choices(string.ascii_letters,k=9))
