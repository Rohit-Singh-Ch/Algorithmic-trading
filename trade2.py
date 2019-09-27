from fyers_api import accessToken
from fyers_api import fyersModel
import pandas as pd
from pandas import DataFrame
import time
import datetime
import time
import xlrd
import requests
from datetime import datetime
from datetime import timedelta
import urllib.request


import os.path
clist = []
mydf=pd.DataFrame(columns=["Symbol","High","Low","Time"])
#import stock3

#Here we generate the authorization_code to authorize the app 
#In visual studio code we have to print the response to get the authorization_code
try:
    app_id = open("api_id.txt", "r").read()  #app_id is given by fyers
except IOError:
    print("api_id.txt file does not exist")

try:
    app_secret = open("app_secret.txt", "r").read()  #app_secret is given by fyers   
except IOError:
    print("app_secret.txt file does not exist")    
app_session = accessToken.SessionModel(app_id, app_secret)
response = app_session.auth()
#print (response)    #to generate authorization_code remove # 
#print("authorization_code -->")
a = response['data']['authorization_code']
#print("a -->", a)

file1 = open("authorization_code.txt", "w")
file1.write(a)
file1.close()





#Now we generate the access token
#you have toh generate the authorization_code after in active
#Again we comment the app_session.generate_token(), we copy the token
try:
    authorization_code = open("authorization_code.txt", "r").read()   
except IOError:
    print("authorization_code.txt file does not exist")
app_session.set_token(authorization_code)
app_session.generate_token()
#print(app_session.generate_token())   #to generate token remove # 


weburl = urllib.request.urlopen(app_session.generate_token())
#print("Token -->",(weburl.info()))
b = weburl.info()
#print(b)
s = b['Location']
#print(s.split('='))
#print(s.split('=')[1])
t=(s.split('=')[1])+"="
#print(t)

file2 = open("token.txt", "w")
file2.write(t)
file2.close()

#Here we check we connected to the api or not
#comment the print(fyers) after check
#you have toh generate the token after in active
try:
    token = open("token.txt", "r").read()   
except IOError:
    print("app_secret.txt file does not exist")
is_async = False #(By default False, Change to True for asnyc API calls.))
fyers = fyersModel.FyersModel(is_async)
#print(fyers)

#Here we check the profile through the token
#comment the print so we can't get again and agian profile
"""profile = fyers.get_profile(token = token)
print(profile)"""

"""data1 = fyers.search_symbols(
token = token,
data = {
"query" : "1100",
"limit" : 30
}
)
print(data1)"""



