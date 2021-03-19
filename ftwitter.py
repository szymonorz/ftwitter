import requests
from requests_oauthlib import OAuth1

consumer_key='3nVuSoBZnx6U4vzUxf5w'
consumer_secret='Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'
oauth_token_key=""
oauth_token_secret=""

headers = {
            'timezone': 'Europe/Warsaw',
            'os-security-patch-level': '2018-01-05',
            'optimize-body': 'true',
            'accept': 'application/json',
            'x-twitter-client': 'TwitterAndroid',
            'x-twitter-fleets-session-id': '1615841187289',
            'user-agent': 'TwitterAndroid/8.83.1-release.03 (28831003-r-3) Android+SDK+built+for+x86/8.1.0 (Google;Android+SDK+built+for+x86;google;sdk_gphone_x86;0;;1;2013)',
            'x-twitter-client-adid': 'a10c9956-3a4d-499a-815b-c7f7b62f733e',
            'accept-encoding': 'zstd, gzip, deflate',
            'x-twitter-client-language': 'en-US',
            'x-client-uuid': '7e8c7231-46a2-4d31-895a-739864171c0d',
            'x-twitter-client-deviceid': '6f248cf231f26378',
            'x-twitter-client-version': '8.83.1-release.03',
            'cache-control': 'no-store',
            'x-twitter-active-user': 'yes',
            'x-twitter-api-version': '5',
            'x-twitter-client-limit-ad-tracking': '0',
            'kdt': 'yOwqOg1fzpEbt05Kn4S6N4usLuZtV5Ef3lgZLQGb',
            'x-b3-traceid': '5749a83b45ed7660',
            'accept-language': 'en-US',
            'x-twitter-client-flavor':'', 
            'cookie': 'personalization_id=v1_oZDk98plmgflODXz5EC9Cw==; guest_id=v1%3A161584107840537238',
            'content-length': '0'
}


def get_token(identifier, password):
    cookie = 'personalization_id=v1_io+IeH5rlE+7tiQYUPWy2A==; guest_id=v1%3A161572374901410511; lang=en'
    url = "https://api.twitter.com/auth/1/xauth_password.json"
    guest_url="https://api.twitter.com/1.1/guest/activate.json"
    headers = {
            'x-twitter-client-deviceid':'6f248cf223f26378',
            'x-twitter-client-adid':'a10c9956-3a4d-499a-815b-c7f7b62f733e',
            'x-twitter-client-language':'en-US',
            'authorization':'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F',
            'x-twitter-client-version':'8.83.1-release.03',
            'content-type':'x-www-form-urlencoded',
            'x-client-uuid':'7e8c7231-46a2-4d31-895a-739864171c0d',
            'accept':'application/json',
            'x-twitter-client':'TwitterAndroid',
            'user-agent':'TwitterAndroid/8.83.1-release.03 (28831003-r-3) Android+SDK+built+for+x86/8.1.0 (Google;Android+SDK+built+for+x86;google;sdk_gphone_x86;0;;1;2013)',
            'x-twitter-active-user':'yes',
            'x-twitter-api-version':'5',
            'kdt':'yOwqOg1fzpEbt05Kn4S6N4usLuZtV5Ef3lgZLQGb',
            'x-b3-traceid':'3ad2a2513da12fac',
            'x-twitter-client-limit-ad-tracking':'0',
            'accept-language':'en-US',
            'x-twitter-client-flavor':'',
            'cookie': cookie }

    data = {
        'x_auth_identifier':identifier,
        'x_auth_password':password
    }

    g = requests.post(guest_url, headers=headers)
    token = g.json()
    headers['x-guest-token']=g.json()['guest_token']

    r = requests.post(url, params=data, headers=headers)
    print(r)
    code = r.status_code
    if code != 200:
        print(r.json())
        print("Error while attempting to login, check other steps")
    else:
        json = r.json()
        if hasattr(json, 'errors') or hasattr(json,'login_verification_request_id'):
            print(json)
        else:
            global oauth_token_key
            global oauth_token_secret
            oauth_token_key=r.json()['oauth_token']
            oauth_token_secret=r.json()['oauth_token_secret']
            print('oauth_token_key: '+oauth_token_key)
            print('oauth_token_secret: '+oauth_token_secret)
            print("Copy your oauth_token and secret and write them into the file")
            print("then you won't have to go through the login process again in the future")

def get_fleets(user_id, auth):
        global headers
        url="https://api.twitter.com/fleets/v1/user_fleets"
        params = {
            'user_id':user_id,
        }


        fleet_r = requests.get(url, headers=headers, params=params, auth=auth)
        code = fleet_r.status_code
        if code == 200:
            fleet_json = fleet_r.json()
            fleets_threads = fleet_json['fleet_threads']
            for T in fleets_threads:
                for F in T['fleets']:
                    print(F['media_entity']['media_url_https'])
        elif code == 403:
            print("Action forbidden")
            print("Either Twitter blocked your IP address or the account you're trying to view is private")
        elif code == 401:
            print("Unauthorized")
            print("Make sure your oauth_token_key and oauth_token_secret variables are correct")
        else:
            print("Error")


def get_user(string, auth, isID):
    global headers
    if isID:
        params= {"user_id": string}
    else:
        params={"screen_name": string}

    r = requests.get("https://api.twitter.com/1.1/users/lookup.json", params=params, headers=headers, auth=auth)
    print(r)
    if r.status_code !=200:
        print(r.json())
        return ()
    else:
        j = r.json()[0]
        return (j['screen_name'],j['id'])

def login():
    if not oauth_token_key or not oauth_token_secret:
        print("Oauth token not present")
        print("Initiating login....")
        identifier = input("Login: ")
        password = input("Password: ")
    if not identifier or not password:
        print("No password or login detected")
        print("Exiting program")
        return
    else:
        get_token(identifier, password)

def get(command, var):
    auth = OAuth1(consumer_key,consumer_secret,oauth_token_key,oauth_token_secret)
    if command == 'fleets' or command == 'f' and var:
        user = get_user(var, auth, var.isdigit())
        if not user:
            print("User not found or other error. Check JSON message above")
        else:
            print(f"{user[0]}'s fleets: ")
            get_fleets(user[1],auth)
    elif command == 'fleets' or command == 'f' and not var:
        print("Command 'get fleets' requires user_id or @ handle as an argument")
    elif command == "blockedby" or command == "bb":
        print("Not available (yet)")
    else:
        print("Available commands: \n login (l) \n get fleets (f) \n get blockedby (bb) \n exit (e)")



def start_cmd():
    while True:
        command = input("ftwitter> ")
        args = command.split(' ')
        first = args[0]
        if first == 'login' or first == 'l':
            login()
        elif first == 'get':
            if not oauth_token_key or not oauth_token_secret:
                print("Oauth token not present")
                print("First call login before any other action")
            else:
                if len(args)==3:
                    get(args[1],args[2])
                elif len(args)==2:
                    get(args[1],"")
                else:
                    print("Wrong ammount of arguments")


        elif first == 'exit' or first == 'e':
            break;
        else:
            print("Command not found")
            print("Available commands: \n login (l) \n get fleets (f) \n get blockedby (bb) \n exit (e)")
    print("Exiting ftwitter...")



if __name__ == '__main__':
    start_cmd()
