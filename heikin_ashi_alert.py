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
date_time = ""
logger = ""


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
    
######## SYMBOL FETCHING DATA FUNCTION START ###########    
#This is datafetch function which fetch the historical data of 1 min & we consolidate the 1 min data to 15 min data
#We call the fileread function here to read the excel file 
def datafetch(fr,to,tim, df3):
    global date_time
    newdf = pd.DataFrame()
    for row in df3.iterrows():
        global name
        name=row[1][0]
        stock="NSE:"+name+"-EQ"
        op=row[1][1]
        cl=row[1][2]
        cashValue=row[1][3]
       
           
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
        lowerlimit=0
        upperlimit=0
        
        df = pd.DataFrame(data1['data']) 
    
        ct=df['o'].count()
        
        loop = int(ct/tim)
       
        for i in range(int(loop)):
            
            hour=9
            minute=15
            lowerlimit=tim*i+0
                
            upperlimit=tim*(i+1)-1
            minute=minute+(i+1)*tim
            hour=hour+int(minute/60)
            
            minute=minute%60
            for _ in df[lowerlimit:upperlimit+1]:
                cl=df.at[upperlimit,'c']
                hi=max(df[lowerlimit:upperlimit+1]['h'])
                #print ("hi -->", hi)
                low=min(df[lowerlimit:upperlimit+1]['l'])
                op=df.at[lowerlimit,'o']
            #ran=abs(hi-low)
            #body=abs(op-cl)
            #half=ran/2
        newdf = newdf.append({'CashValue': cashValue, 'Symbol':row[1][0],'Open' : op, 'High' : hi, 'Low' : low, 'Close' : cl, 'Time' : datetime.fromtimestamp(int(fr))},  ignore_index = True)
    HA(newdf, cashValue, stock, fr)           
    
######## SYMBOL FETCHING DATA FUNCTION END ###########    
   
####### HEIKIN ASHI FUNCTION START #############   
# This is Heikin Ashi function were we convert the 15min consolidate data into heikin ashi candle
# Heikin ashi candle values are based on the Heikin ashi fourmulas
# There are total 4 fourmulas in which 3 are simple but to calculate the Heikin ashi Open first candle we have to take previous day Heikin ashi (Open + Close)/2
# Therefore we store Heikin ashi Open & Close value into StockList.xls file
# In this function we generate the alert system and get a alert on telegram
ovalue = []				
cvalue = []

def HA(df, cashValue, stock, fr):
    cna=""
    ha_cl = (df['Open']+ df['High']+ df['Low']+df['Close'])/4.0
    ha_cl1 = round(ha_cl/ 0.05) * 0.05
    df['HA_Close'] = round(ha_cl1, 2)
    
    workbook = xlrd.open_workbook('StockList.xls')
    worksheet = workbook.sheet_by_name('Sheet1')
    idx = df.index.name
    df.reset_index(inplace=True)
    temp=1	
    for i in range(0, len(df)):
        if (str(df.iloc[i]['Time']) == date_time):
            ha_op = (worksheet.cell_value(temp, 1) + (worksheet.cell_value(temp, 2))) / float(2)
            ha_op1 = round(ha_op/ 0.05)*0.05
            df.set_value(i, 'HA_Open', ha_op1)
            temp = temp + 1
            ovalue.append(df.iloc[i]['HA_Open'])
            cvalue.append(df.iloc[i]['HA_Close'])
            

        else:
            ha_op = (ovalue[i] + cvalue[i]) / float(2)
            ha_op1 = round(ha_op/ 0.05) * 0.05
            df.set_value(i, 'HA_Open', ha_op1)
            ovalue[i] = df.iloc[i]['HA_Open']
            cvalue[i] = df.iloc[i]['HA_Close']
            
   

    if idx:
        df.set_index(idx, inplace=True)

    ha_hi = df[['HA_Open','HA_Close','High']].max(axis=1)
    ha_hi1 = round(ha_hi/ 0.05) * 0.05
    df['HA_High']= round(ha_hi1, 2)
    
    ha_low = df[['HA_Open','HA_Close','Low']].min(axis=1)
    ha_low1 = round(ha_low/ 0.05) * 0.05
    df['HA_Low']=round(ha_low1, 2)
    df = df.reindex(columns=['Symbol','Open','High','Low','Close','HA_Close','HA_High','HA_Low','HA_Open','Time', 'CashValue'])
    #print(df)
    
    # Get full path for writing.
    name = "HA_OUTPUT-" + str(date.today()) + ".txt"
    with open(name, "a") as f:
        # Write data to file.
        f.write(str(df))    
    

    for r in range(len(df)):
        ran=float(abs(df.iloc[r]['HA_High']-df.iloc[r]['HA_Low']))
        body=float(abs(df.iloc[r]['HA_Open']-df.iloc[r]['HA_Close']))
        half=ran/5
        cna = df.iloc[r]['Symbol'] #Isme for loop abhi jis company ka naam read kr rha h uska naam h (symbol)
        cashValue = worksheet.cell_value(r+1, 3) #excel symbol location + increment
        if cna not in clist:
            if body > half and(cashValue/2) < ran <= (cashValue*1.01):         #ran <= cashValue
                company = ("STOCK = "+df.iloc[r]['Symbol'])
                a = ("Date and Time="+str(datetime.fromtimestamp(int(fr))))
                clist.append(df.iloc[r]['Symbol'])
                telegram(a,company,(df.iloc[r]['HA_Close']),(df.iloc[r]['HA_High']),(df.iloc[r]['HA_Low']),(df.iloc[r]['HA_Open']))

####### HEIKIN ASHI FUNCTION END #############            
            
            
        
####THIS IS A TELEGRAM FUNCTION ########
# This is a telegram function which is use only to generate the alert on channel #@algotradealert (Channel name)
def telegram(a,company,cl,hi,low,op):
    bot_token = '986625783:AAEmqQ2WVKVi3TgYn79Fd5aYvXoSKdObRZw'
    bot_chatID = '-1001346495883'  #paste your chatid where you want to send alert(group or channel or personal)
    bot_message = company + "\n" + a + "\n" + "Open =" +  str(op) + "\n" + "High =" + str(hi) + "\n" + "Low =" + str(low) + "\n" + "Close =" + str(cl)
    

    # Get full path for writing.
    name = "ALERT_OUPUT-" + str(date.today()) + ".txt"
    with open(name, "a") as f:
        # Write data to file.
        f.write(bot_message)

    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

       
    
    

##### TELEGRAM FUNCTION END #########     

#This is time & date converter function
# To fectch the historical data by using fyers api we have to take Unix timestamp time format which a little bit difficult to understand
# So here we firstaly convert the local_time into Unix timestamp and send it to the datafetch function and then print the local_time
def timeconvert(df3):
    global date_time
   
    now = datetime.today() - timedelta(days=1)  #if you want to work on previoius day data
    
    #now = datetime.now()  #for current day data
    



    dti=now.strftime("%Y-%m-%d")
    date_time=dti+" 09:15:00"
    pattern = '%Y-%m-%d %H:%M:%S'
    fr = int(time.mktime(time.strptime(date_time, pattern)))
    fr=str(fr)
    
    
    dt_string = now.strftime("%d.%m.%Y")
    dt_string = now.strftime("%d.%m.%Y")+" 09:25:00"
    pattern = '%d.%m.%Y %H:%M:%S'
    to = int(time.mktime(time.strptime(dt_string, pattern)))
    to=str(to)
    
    
    tim=10 # time change time is now 10
    
    for _ in range(42):
        
        datafetch(fr,to,tim,df3)
        fr=str(int(fr)+600)
        to=str(int(to)+600)
        time.sleep(1)

fileread()




