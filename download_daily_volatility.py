import requests
import shutil


#Download Daily_Volatility function
def callme():
    url = "https://www.nseindia.com/archives/nsccl/volt/CMVOLT_03102019.CSV"
    r = requests.get(url, verify=False,stream=True)
    if r.status_code!=200:
        print ("Failure!!")
        exit()
    else:
        r.raw.decode_content = True
        with open("Daily_Volatility.csv", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print ("Success")

if __name__ == '__main__':
    callme()

#Download Daily_Volatility function
