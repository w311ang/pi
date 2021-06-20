import requests
import time
import random

token='lwSTISLtFxgKaic-2Wbo60yZDIdZeGg3xWmSVhdc1Sk'
api='https://socialchain.app'
timing=False

session=requests.Session()
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
    print(error)
  except:
    pass
  raise Exception(str(prstatus)+'未知错误')
