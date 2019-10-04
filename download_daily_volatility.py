#30min and 5mins close>high or close< low
from fyers_api import accessToken
from fyers_api import fyersModel
import pandas as pd
from pandas import DataFrame
import time
import datetime
import xlrd
import requests
from datetime import datetime
from datetime import timedelta
from datetime import date
import schedule
import os.path
import logging
import os
import xlsxwriter
from openpyxl import Workbook
import requests
import shutil
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



#Now we generate the access token
#you have to generate the authorization_code after in active
#Again we comment the app_session.generate_token(), we copy the token
try:
    authorization_code = open("authorization_code.txt", "r").read()   
except IOError:
    print("authorization_code.txt file does not exist")
app_session.set_token(authorization_code)
app_session.generate_token()
#print(app_session.generate_token())   #to generate token remove #

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

op=0
cl=0
stock = ""
name=""
#This is fileread function which read the excel file where we store the Symbol, Cash value, Heikin Ashi (open & close)
def fileread():
    try:
        excel_file = 'StockList.xls' #file present in same directory so its realtive path
        
    except IOError:
        print("StockList.xls' file does not exist")
    df3 = pd.read_excel(excel_file)
    timeconvert(df3)

#Previous day high & low value function
def datafetch(fr,to,tim,df3):
    
    newdf = pd.DataFrame()
    for row in df3.iterrows():
        global name
        name=row[1][0]
        stock="NSE:"+name+"-EQ"
        if name not in clist:
            data1 = fyers.get_historical_OHLCV(
            token = token,
            data = {
            "symbol" : stock,
            "resolution" : "1",
            "From" :fr ,
            "to" :to
           }
           )
            i=0
            lo=0
            up=0
            df = pd.DataFrame(data1['data']) 
            ct=df['o'].count()
            loop = int(ct/tim)
            for i in range(int(loop)):
                lo=tim*i+0
                up=tim*(i+1)-1
                for _ in df[lo:up+1]:
                    cl=df.at[up,'c']
                    hi=max(df[lo:up+1]['h'])
                    low=min(df[lo:up+1]['l'])
                    op=df.at[lo,'o']
                ran=abs(hi-low)
                print("Range -->", ran)    
            newdf = newdf.append({'Symbol':row[1][0],'Open' : op, 'High' : hi, 'Low' : low, 'Close' : cl, 'Time' : datetime.fromtimestamp(int(fr))},  ignore_index = True)
            newdf = newdf.reindex(columns=['Symbol','Open','High','Low','Close','Time'])
    print(newdf)






def timeconvert(df3):
   
    #now = datetime.today() - timedelta(days=1)
    now = datetime.now()
    
    dti=now.strftime("%d.%m.%Y")
    
    date_time=dti+"  09:45:00"
    pattern = '%d.%m.%Y %H:%M:%S'
    fr = int(time.mktime(time.strptime(date_time, pattern)))
    fr=str(fr)

    dt_string = now.strftime("%d.%m.%Y")
    dt_string = now.strftime("%d.%m.%Y")+"  10:15:00"
    pattern = '%d.%m.%Y %H:%M:%S'
    to = int(time.mktime(time.strptime(dt_string, pattern)))
    to=str(to)
    
    tim = 30
    datafetch(fr,to,tim,df3)
    time.sleep(1)


fileread()


#Download Daily_Volatility function
def daily_volatility_download():
    tim = datetime.datetime.now()
    url = "https://www.nseindia.com/archives/nsccl/volt/CMVOLT_" + str(tim.strftime('%d')) + "" + str(tim.strftime('%m')) + "" + str(tim.strftime('%Y')) + ".CSV"
    print("url -->", url)   
    r = requests.get(url, verify=False,stream=True)
    if r.status_code!=200:
        print ("Failure!!")
        exit()
    else:
        r.raw.decode_content = True
        with open("Daily_Volatility.csv", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print ("Success")

    data = pd.read_csv("Daily_Volatility.csv")  
        
    # list(data) or 
    list(data.columns) 
    print(list)
       

if __name__ == '__main__':
    daily_volatility_download()

#Download Daily_Volatility function

    
#844347012(upendra chat id)
#@algotradealert (Channel name)