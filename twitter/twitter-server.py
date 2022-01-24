import oauth2
import json
import os
import urllib
from flask import request, Response, Flask

app = Flask(__name__)
app.config["DEBUG"] = True

CONSUMER_KEY='XXXXX'
CONSUMER_SECRET='XXXXX'

ACCESS_TOKEN='XXXXXX'
ACCESS_TOKEN_SECRET='XXXXXX'

def oauth_req(url, key, secret, http_method="GET", post_body=b"", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers )
    
    return content, resp

def json_str(json_obj):
    return json.dumps(json_obj, indent=2, sort_keys=True)


def get_account_settings():
    home_timeline = oauth_req('https://api.twitter.com/1.1/account/settings.json', ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #data = home_timeline.decode('utf-8', 'replace')
    data = home_timeline[0]
    obj = json.loads(data)

    print(json_str(obj))

def get_timeline():
    home_timeline = oauth_req('https://api.twitter.com/1.1/statuses/home_timeline.json', ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #data = home_timeline.decode('utf-8', 'replace')
    data = home_timeline[0]
    obj = json.loads(data)

    return json_str(obj)

def get_friends():
    home_timeline = oauth_req('https://api.twitter.com/1.1/friends/list.json', ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #data = home_timeline.decode('utf-8', 'replace')
    data = home_timeline[0]
    obj = json.loads(data)

    return json_str(obj['users'])

def get_tweets(user_id=None, screen_name=None, tweet_id=None):
    params = ''

    if screen_name != None or user_id != None or tweet_id != None:
        params = '?'

    if screen_name != None:
        params += 'screen_name=' + screen_name + "&"

    if tweet_id != None:
        params += 'since_id=' + tweet_id + "&count=1&"

    home_timeline = oauth_req('https://api.twitter.com/1.1/statuses/user_timeline.json' + params, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #data = home_timeline[0].decode('utf-8', 'replace')
    data = home_timeline[0]
    obj = json.loads(data)
    return json_str(obj)

def post_tweet(tweet):

    # URLENCODEAR EL TWEET
    params = urllib.parse.urlencode({ 'status': tweet })

    home_timeline = oauth_req('https://api.twitter.com/1.1/statuses/update.json?' + params, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, http_method='POST')

    #data = home_timeline.decode('utf-8', 'replace')
    data = home_timeline[0]
    obj = json.loads(data)
    
    return str(obj['id'])


def delete_tweet(tweet_id):
    home_timeline = oauth_req('https://api.twitter.com/1.1/statuses/destroy/' + tweet_id + '.json', ACCESS_TOKEN, ACCESS_TOKEN_SECRET, http_method='POST')

    #data = home_timeline.decode('utf-8', 'replace')
    data = home_timeline[0]
    obj = json.loads(data)

    return json_str(obj)


# https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
def search_tweets(text):
    params = urllib.parse.urlencode({'q' : text})

    home_timeline = oauth_req('https://api.twitter.com/1.1/search/tweets.json?' + params, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #data = home_timeline.decode('utf-8', 'replace')
    data = home_timeline[0]
    obj = json.loads(data)
    
    # print(json_str(obj['search_metadata']))

    return obj

def send_dm(text, user_id):

    params = '''{"event": 
        {"type": "message_create", "message_create": 
            {"target": 
                {"recipient_id": "''' + user_id  +  '''"}, 
                "message_data": {"text": "''' + text + '''"}}}}
    '''
    params = str(params).encode('utf-8')

    dm, response = oauth_req('https://api.twitter.com/1.1/direct_messages/events/new.json', ACCESS_TOKEN, ACCESS_TOKEN_SECRET, 
        http_method='POST', post_body=params, http_headers={"Content-Type": "application/json"})

    return json_str(json.loads(dm.decode('utf-8', 'replace')))

 
def register_webhook(url):
    params = urllib.parse.urlencode({'url' : url})
    
    wh = oauth_req('https://api.twitter.com/1.1/account_activity/all/development/webhooks.json?' + params,
                  ACCESS_TOKEN, ACCESS_TOKEN_SECRET, http_method='POST')
    
    print(wh)
    #return json_str(json.loads(wh.decode('utf-8', 'replace')))
 
#print(register_webhook('https://integracion-redes-gmbarrera455673.codeanyapp.com/webhook_twitter')) 
 
#print(send_dm("Hola David!!", "39624705"))


# '''
# st = search_tweets('dolar :(')
# for tweet in st['statuses']:
#     print("=" * 60)
#     print(tweet['text'])
# '''


# id = post_tweet('Estamos en la clase de integracion, probando Tweeter v1')
# print(id)

# input('Esperando....')

# r = delete_tweet(id)
# print('Tweet eliminado')



#'660190983573893121'
#'gmbarrera01'

#f = open('tweets.txt', 'w')
# f.write(get_tweets(screen_name='un_usuario'))
#f.write(get_tweets(tweet_id='660190983573893121'))
#f.close()

if __name__ == "__main__":
    #print("Escuchando...")
    #app.run('0.0.0.0')
    #post_tweet('hola')
    #print(get_tweets(screen_name='@dbertolini1987'))
    f = open('tweets.txt', 'w')
    #f.write(get_timeline()) #trae las novedades
    f.write(get_friends())
    #f.write(get_tweets()) #trae los tweets en donde estoy relacionado
    #f.write(get_tweets(tweet_id='660190983573893121')) #no se que trae
    f.close()