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
cname = ""
name=""
#This is fileread function which read the excel file where we store the Symbol, Cash value, Heikin Ashi (open & close)

def fileread():
    excel_file = 'company1.xls' #file present in same directory so its realtive path
    df3 = pd.read_excel(excel_file)

    conv(df3)

def xyz(fr,to,tim, df3,p):
    global mydf
    print("fr=",fr)
    print("to=",to)
    newdf = pd.DataFrame()
    for row in df3.iterrows():
        global name
        name=row[1][0]
        cname="NSE:"+name+"-EQ"
        token="gAAAAABdhc8NbZjewX8v8EZhOiM3RvqATj7TWZ-x_ccwY-Itl72hikJmVmABi92c_khQySt1CzYZPwwDBcWiBX3YoWiFmNQLHabk_HJMcmrbEgczK89vEQA="
        data1 = fyers.get_historical_OHLCV(
        token = token,
        data = {
        "symbol" : cname,
        "resolution" : "1",
        "From" :fr ,
        "to" :to

        }
        )
        
        i=0
        lo=0
        up=0
        print("symbol=",name)
        print("time=",datetime.fromtimestamp(int(fr)))
        df = pd.DataFrame(data1['data']) 
        print("df=")
        print(df)
        ct=df['o'].count()
        
        loop = int(ct/tim)
        print("loop=",loop)
        for i in range(int(loop)):
            print("hellollop")
            ho=9
            mini=15
            lo=tim*i+0
                
            up=tim*(i+1)-1
            mini=mini+(i+1)*tim
            ho=ho+int(mini/60)
            
            mini=mini%60
            for _ in df[lo:up+1]:
                cl=df.at[up,'c']
                hi=max(df[lo:up+1]['h'])
                low=min(df[lo:up+1]['l'])
                op=df.at[lo,'o']
        if loop == 0:
            cl=float(df['c'])
            op=float(df['o'])
            low=float(df['l'])
            hi=float(df['h'])
            
            
        
        newdf = newdf.append({'Symbol':row[1][0],'Open' : op, 'High' : hi, 'Low' : low, 'Close' : cl, 'Time' : datetime.fromtimestamp(int(fr))},  ignore_index = True)
        newdf = newdf.reindex(columns=['Symbol','Open','High','Low','Close','Time'])
           
             
            
    
    print("newdf")
    print(newdf)
    if p==0:
        mydf[["Symbol","High","Low","Time"]]=newdf[["Symbol","High","Low","Time"]]
    else:
        for r in range(len(newdf)):
            ranh=float(newdf.iloc[r]['High'])
            
            bodyh=float(mydf.iloc[r]['High'])
            ranl=float(newdf.iloc[r]['Low'])
            bodyl=float(mydf.iloc[r]['Low'])
                 
            cna = newdf.iloc[r]['Symbol'] 
            
            if cna not in clist:
                if ranh > bodyh:
                    company=("STOCK="+newdf.iloc[r]['Symbol']+" high is broken")
                    print(company)
                    clist.append(newdf.iloc[r]['Symbol'])
                elif ranl < bodyl:
                    company=("STOCK="+newdf.iloc[r]['Symbol']+" low is broken")
                    print(company)
                    clist.append(newdf.iloc[r]['Symbol'])
                    
                """if ranh > bodyh or ranl < bodyl: 
                    company = ("STOCK = "+newdf.iloc[r]['Symbol'])
                    print(company)
                    a = ("Date and Time="+str(datetime.fromtimestamp(int(fr))))
                    clist.append(newdf.iloc[r]['Symbol'])"""
                
    print("Mydf=")
    print(mydf)
       
    




def conv(df3):
   
    #now = datetime.today() - timedelta(days=1)
    #print(now)
    #print(type(now))
    now = datetime.now()
    
    dti=now.strftime("%d.%m.%Y")
    #print("date=",dti)
    
    
    date_time=dti+"  09:15:00"
    pattern = '%d.%m.%Y %H:%M:%S'
    fr = int(time.mktime(time.strptime(date_time, pattern)))
    fr=str(fr)
    tof=fr

    #dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    dt_string = now.strftime("%d.%m.%Y")
    dt_string = now.strftime("%d.%m.%Y")+"  09:45:00"
    #print("date and time =", dt_string)
    pattern = '%d.%m.%Y %H:%M:%S'
    to = int(time.mktime(time.strptime(dt_string, pattern)))
    to=str(to)
   
    
    tim = 30
    
    for p in range(331):
        xyz(fr,to,tim,df3,p)
        print("fr=previous",fr)
        if(fr == tof):
            fr=str(int(fr)+1800)
            to=fr
            print("hello")
            print(fr)
            print(to)
        else:
            fr=str(int(fr)+60)
            to=fr
            #print("fr=",fr)
            #print("to=",to)
           #print(fr)
           #print(to)
            
        time.sleep(1)


fileread()

#844347012(upendra chat id)
#@algotradealert (Channel name)
