import codechef_cli.api.codechef as ccapi

def test_oauth():
    x = ccapi.Codechef("a5a5697c8f2bfcbc816635b0e6c05b83","1247a2aa0a2f37f00003a3fe9d15a2d3")
    x.start_oauth_flow()
    assert(x.tokens!=None)

