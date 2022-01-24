from flask import Flask, request
import json
import requests 

bot_token = 'XXXXXX'

app = Flask(__name__)
app.config['TESTING'] = True
app.config['DEVELOPMENT'] = True
app.config['DEBUG'] = True

#@app.route('/hola', methods=['POST', 'GET'])
#def hola():
#  print('holaXXX')
#  return '200'

@app.route('/hooktelegram', methods=['POST', 'GET'])
def hook_telegram():
  data = request.json
  print(data['message']['text'])
  
  message = input('Ingrese mensaje: ')
  if message != '':
      payload = {'chat_id': data['message']['chat']['id'] , 'text': message }
      headers = {
          'Content-Type': "application/json",
          }

      response = requests.post('https://api.telegram.org/bot' + bot_token + '/sendMessage', headers=headers,json=payload)
      data = json.loads(response.text)
      if data['ok']:
          print(response.text)
  print('-' * 50)
  
  return '200'

if __name__ == "__main__":
  app.run('0.0.0.0', port=3000)
