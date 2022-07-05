
import requests
from bs4 import BeautifulSoup
import time
import smtplib



#url of the product
URL = 'https://www.amazon.in/OnePlus-Nord-Lite-128GB-Storage/dp/B09WQYFLRX/?_encoding=UTF8&pd_rd_w=jBUhF&content-id=amzn1.sym.e0e8ce89-ede3-4c51-b6ad-44989efc8536&pf_rd_p=e0e8ce89-ede3-4c51-b6ad-44989efc8536&pf_rd_r=S944Q3F2AQ1NR8MW31Q7&pd_rd_wg=pkcYR&pd_rd_r=592dac07-da0b-4261-829f-337424b722c2&ref_=pd_gw_ci_mcx_mr_hp_d'
#just google my user agent to get thsi
myheader = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


#fundtion to check the price of the product
def price_check():
    #request to get the html content of the page
    webpage = requests.get(URL, headers=myheader)
    
    #make a tree like structre using a parser to make search easy
    soup = BeautifulSoup(webpage.content, 'html.parser')

    title = soup.find(id='productTitle').get_text()
    price = soup.find(class_="a-price-whole").get_text()#here we search using class_ as class is a reserved word in python
    price = price.replace(",", "")
    price = price.replace(".", "")
    floatprice = float(price[0:6])

    #strip to remove extra spaces
    print(title.strip())
    print(floatprice)
    if(floatprice < 17000):
        notify()


# function to send the mail
def notify():
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('senders mail id@gmail.com', 'pasword')

    subject = 'Buy it Now!!'
    body = 'the price of the product you were checking fell down!! BUY IT!! : https://www.amazon.in/OnePlus-Nord-Lite-128GB-Storage/dp/B09WQYFLRX/?_encoding=UTF8&pd_rd_w=jBUhF&content-id=amzn1.sym.e0e8ce89-ede3-4c51-b6ad-44989efc8536&pf_rd_p=e0e8ce89-ede3-4c51-b6ad-44989efc8536&pf_rd_r=S944Q3F2AQ1NR8MW31Q7&pd_rd_wg=pkcYR&pd_rd_r=592dac07-da0b-4261-829f-337424b722c2&ref_=pd_gw_ci_mcx_mr_hp_d'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'senders mail id',
        'recivers mail id',
        msg
    )
    print('Email is sent!!')

    server.quit()




while(True):
    price_check()
    time.sleep(60*60*2)



