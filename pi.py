import requests
import time
import random
import os
import pickle

api='https://socialchain.app'

on=os.getenv('on')
if on=='schedule':
  timing=True
else:
  timing=False
userpass=os.getenv('userpass')
userpass=userpass.split()
username=userpass[0]
password=userpass[1]
try:
  with open('tokens.txt','rb') as f:
    tokens=pickle.load(f)
    token=tokens[username]
except FileNotFoundError:
  tokens={}
  token=''
except KeyError:
  pass
session=requests.Session()
if session.get(api+'/api/pi').status_code!=200:
  login=session.post(api+'/api/password_sign_in',data={'phone_number':username,'password':password}).json()
  token=login['credentials']['access_token']
  with open('tokens.txt','wb') as f:
    tokens[username]=token
    pickle.dump(tokens,f)
session.headers.update({'authorization':'Bearer '+token})

expires=False
while not expires:
  if timing==True:
    time.sleep(60)
  else:
    time.sleep(3)
  me=session.get(api+'/api/pi').json()
  is_mining=me['mining_status']['is_mining']
  #is_mining='false'
  if is_mining=='false':
    expires=True

if timing==True:
  thetime=random.randint(5,20)
  time.sleep(thetime*60)
  print('随机等待%smin'%thetime)

proof=session.post(api+'/api/proof_of_presences',data={'recaptcha_token':None})
prstatus=proof.status_code
if prstatus==200:
  print('续期成功')
elif prstatus==500:
  prjson=proof.json()
  raise Exception(prjson['error'])
elif prstatus==401:
  raise Exception('token已过期')
else:
  try:
    prjson=proof.json()
    error=prjson['error']
    raise Exception('%s %s'%(prstatus,error))
  except json.decoder.JSONDecodeError:
    raise Exception(str(prstatus)+'未知错误')
