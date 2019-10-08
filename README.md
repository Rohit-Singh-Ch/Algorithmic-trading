# Algorithmic-trading

1. First install the python software..(name)
2. Fyers API is a set of rest APIs that provide integration with our in-house trading platform with which you can build your ow       	      customized trading applications.
3. To use fyers APIs, user will be required to create an app from the API Dashboard.
4. Once user have created our app, he will be provided with an App Id and Secret Id.
5. After creating this app,user have to install fyers api.
6. API Key And API Secret are used to authenticate the application and to prevent unauthorised usage.
7. To fetch the data from fyers,we have to create an app.
8. Authentication is done via oAuth process.
9. The authorization is a 5 steps process as explained below.

       + Client initiates a request to get token for his app
       + An authorization code will be returned if the app_id and secret_id is valid from the above request
       + Paste the authorization code to authorization_code.txt file
       + If the above request succeed, the user will be redirected to the login page to authorize the app
       + User will provide login credentials which will be validated from the server
       + On successfully validating the credentials, access_token will be generated and redirect users to the page specified in app 		 dashboard
       + Paste the access_token to access_token.txt file
	
10. All the file you have to keep in folder name Algo trading
       
       + OHLCV_30min_alert.py
       + heikin_ashi_alert.py
	  + fyers_authorization.py
       + download_daily_volatility.py
       + StockList.xls
	  + StockList_30.xls
       + api_id.txt
       + app_secret.txt
       + authorization_code.txt
       + token.txt
	  
	  
	  EXTENSION OF THE EXCEL SHOULD BE .xls(!important)
