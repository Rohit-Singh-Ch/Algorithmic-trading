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


def fileread():
    excel_file = 'StockList_30min.xls' #file present in same directory so its realtive path
    df3 = pd.read_excel(excel_file)

    timeconvert(df3)

def datafetch(fr,to,tim, df3,p):
    global mydf
    
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
            newdf = newdf.append({'Symbol':row[1][0],'Open' : op, 'High' : hi, 'Low' : low, 'Close' : cl, 'Time' : datetime.fromtimestamp(int(fr))},  ignore_index = True)
            newdf = newdf.reindex(columns=['Symbol','Open','High','Low','Close','Time'])
    print(newdf)
    if p==0:
        mydf[["Symbol","High","Low","Time"]]=newdf[["Symbol","High","Low","Time"]]
    else:
        for r in range(len(newdf)):
            close=float(newdf.iloc[r]['Close'])
            high=float(mydf.iloc[r]['High'])
            low=float(mydf.iloc[r]['Low'])
            cna = newdf.iloc[r]['Symbol'] 
            if close > high:
                company=("STOCK="+newdf.iloc[r]['Symbol']+" close is greater than high")
                print(company)
                a = ("Date and Time="+str(datetime.fromtimestamp(int(fr))))
                clist.append(newdf.iloc[r]['Symbol'])
                telegram(company, close, high, low,a)
            elif close < low:
                company=("STOCK="+newdf.iloc[r]['Symbol']+" close is less than low")
                print(company)
                a = ("Date and Time="+str(datetime.fromtimestamp(int(fr))))
                clist.append(newdf.iloc[r]['Symbol'])
                telegram(company, close, high, low,a)


####THIS IS A TELEGRAM FUNCTION ########
# This is a telegram function which is use only to generate the alert on channel #@algotradealert (Channel name)
def telegram(company, close, high, low,a):
    bot_token = '986625783:AAEmqQ2WVKVi3TgYn79Fd5aYvXoSKdObRZw'
    bot_chatID = '-1001346495883'  #paste your chatid where you want to send alert(group or channel or personal)
    bot_message = company + "\n"  +  str(close) + "\n" + "High =" + str(high) + "\n" + "Low =" + str(low) +  "\n" + "Time =" + a
    
    # Get full path for writing.
    name = "30min_ALERT_OUPUT-" + str(date.today()) + ".txt"
    with open(name, "a") as f:
        # Write data to file.
        f.write(bot_message)
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

##### TELEGRAM FUNCTION END #########      




def timeconvert(df3):
   
    #now = datetime.today() - timedelta(days=1)
    now = datetime.now()
    
    dti=now.strftime("%d.%m.%Y")
    
    date_time=dti+"  09:15:00"
    pattern = '%d.%m.%Y %H:%M:%S'
    fr = int(time.mktime(time.strptime(date_time, pattern)))
    fr=str(fr)
    tof=fr

    dt_string = now.strftime("%d.%m.%Y")
    dt_string = now.strftime("%d.%m.%Y")+"  09:45:00"
    pattern = '%d.%m.%Y %H:%M:%S'
    to = int(time.mktime(time.strptime(dt_string, pattern)))
    to=str(to)
    
    tim = 30
    
    for p in range(331):
        datafetch(fr,to,tim,df3,p)
        if(fr == tof):
            fr=str(int(fr)+1800)
            to=str(int(to)+300)
        else:
            fr=str(int(fr)+300)
            to=str(int(to)+300)
        tim=5    
            
        time.sleep(1)


fileread()

#844347012(upendra chat id)
#@algotradealert (Channel name)


