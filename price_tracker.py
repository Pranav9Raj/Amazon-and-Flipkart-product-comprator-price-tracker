
import requests
import smtplib                     #simple mail transfer protocol
from bs4 import BeautifulSoup      #for web scraping
import time 


# Put the URL of product of which you need to keep track of

# Amazon link
product_URLa = "https://www.amazon.in/Apple-MacBook-Chip-13-inch-256GB/dp/B08N5XSG8Z/ref=lp_10559548031_1_1"
# Flipkart link
product_URLf = "https://www.flipkart.com/apple-2020-macbook-air-m1-8-gb-256-gb-ssd-mac-os-big-sur-mgn63hn-a/p/itmde54f026889ce?pid=COMFXEKMGNHZYFH9&lid=LSTCOMFXEKMGNHZYFH9P56X45&marketplace=FLIPKART&q=macbook+air+laptop+apple+m1+chip&store=6bo&srno=s_1_3&otracker=AS_Query_OrganicAutoSuggest_1_33_na_na_ps&otracker1=AS_Query_OrganicAutoSuggest_1_33_na_na_ps&fm=search-autosuggest&iid=8e373a6c-e452-401e-9fab-51c15945247e.COMFXEKMGNHZYFH9.SEARCH&ppt=sp&ppn=sp&ssid=oz7x8p4shs0000001657087829144&qH=c181b31cee16abe4"

# Define header and pass your user agent info to header
Header = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

threshold = 92000.0      #threshold value to set for product 

def mail(a: float, f: float):

    Setserver=smtplib.SMTP('smtp.gmail.com',587)    #establish connection gmail and our server
    Setserver.ehlo()           
    Setserver.starttls()                            #encrpts the code
    Setserver.ehlo()

    Setserver.login('senders email', 'password')    #pass the login credentials to send the mail

    Subject ='Price Got Dropped!!!'                 #Subject of the Mail

    Body_Amazon = 'Hurry Up!!! Check it out.... The Prices are Down - https://www.amazon.in/Apple-MacBook-Chip-13-inch-256GB/dp/B08N5XSG8Z/ref=lp_10559548031_1_1 '
    Body_Flipkart = 'Hurry Up!!! Check it out.... The Prices are Down - https://www.flipkart.com/apple-2020-macbook-air-m1-8-gb-256-gb-ssd-mac-os-big-sur-mgn63hn-a/p/itmde54f026889ce?pid=COMFXEKMGNHZYFH9&lid=LSTCOMFXEKMGNHZYFH9P56X45&marketplace=FLIPKART&q=macbook+air+laptop+apple+m1+chip&store=6bo&srno=s_1_3&otracker=AS_Query_OrganicAutoSuggest_1_33_na_na_ps&otracker1=AS_Query_OrganicAutoSuggest_1_33_na_na_ps&fm=search-autosuggest&iid=8e373a6c-e452-401e-9fab-51c15945247e.COMFXEKMGNHZYFH9.SEARCH&ppt=sp&ppn=sp&ssid=oz7x8p4shs0000001657087829144&qH=c181b31cee16abe4 '

    if(f>a):
        message = f"Subject: {Subject}\n\n{Body_Amazon}"            #Format of the Mail to be send

    else:
        message = f"Subject: {Subject}\n\n{Body_Flipkart}"

    Setserver.sendmail('Senders Email','Receivers Email', message)
    print('Email is sent!!!')

    Setserver.quit()


def check_price():
        
    #Here we create a response object 'page' which will store the request-response.
    pagea = requests.get(product_URLa, headers=Header)
    pagef = requests.get(product_URLf, headers=Header)

    #parse the data from HTML
    soupa = BeautifulSoup(pagea.content, 'html.parser')
    soupf = BeautifulSoup(pagef.content, 'html.parser')

    #Get the name and price of product from amazon website using soup.find()
    product_namea = soupa.find(id='productTitle').get_text()           #to get necessary text and not extra info
    product_namef = soupf.find(class_='B_NuCI').get_text()             #to get necessary text and not extra info

    present_pricea = soupa.find(class_="a-price-whole").get_text()
    present_pricef = soupf.find(class_="_30jeq3 _16Jk6d").get_text()
    
    #For Amazon
    present_pricea = present_pricea.replace(",", "")                  #removes the ',' from presenr_price string
    present_pricea = present_pricea[0:5]                              #extract the required number of characters from string
    present_pricea = float(present_pricea[0:5])                       #returns floating point from string
    #For Flipkart
    present_pricef = present_pricef.replace(",", "")                  #removes the ',' from presenr_price string
    present_pricef = present_pricef.replace("₹", "")                  #removes the '₹' from presenr_price string
    present_pricef = present_pricef[0:5]                              #extract the required number of characters from string
    present_pricef = float(present_pricef[0:5])                       #returns floating point from string

    
     #comapres the best possible Deal
    if(int(present_pricea) < int(threshold) or int(present_pricef) < int(threshold) ):    
        if(int(present_pricef) > int(present_pricea)):
            print(present_pricea)  
            print(product_namea.strip())   # strips out extra spaces
            mail(present_pricea, present_pricef)

        else:
            print(present_pricef)  
            print(product_namef.strip())   # strips out extra spaces
            mail(present_pricea, present_pricef)
    
    
 #Function call Every 2hrs
 while(True)
    check_price()         #Function call
    time.sleep(60*60*2)   #Check eveys 2hrs


