import requests
import time
import random
import os
import pickle
import dateutil.parser

api='https://socialchain.app'

def tostamp(timestr):
  dt = dateutil.parser.parse(timestr)
  stamp=int(time.mktime(dt.timetuple()))
  return stamp

on=os.getenv('on')
if False:
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
  token=''
session=requests.Session()
session.headers.update({'authorization':'Bearer '+token})
if session.get(api+'/api/pi').status_code!=200:
  login=session.post(api+'/api/password_sign_in',data={'phone_number':username,'password':password}).json()
  token=login['credentials']['access_token']
  with open('tokens.txt','wb') as f:
    tokens[username]=token
    pickle.dump(tokens,f)

expires=False
while not expires:
  if timing==True:
    time.sleep(60)
  else:
    time.sleep(3)
  me=session.get(api+'/api/pi').json()
  is_mining=me['mining_status']['is_mining']
  if is_mining==True:
    expires_at=me['mining_status']['expires_at']
    #print(expires_at)
    expires_at=tostamp(expires_at)
    now=time.time()
    diff=expires_at-now
    #print(diff)
    if diff>60*60:
      print('过期时间超过一小时')
      exit()
  #print(is_mining)
  #is_mining='false'
  if is_mining==False:
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
