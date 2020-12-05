#imports for our API
import requests
import json
#imports for our email
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#part1: API
#get api key from tankerkoenig and define parameters in url
#I set lat & lng to my location aswell as an rad of 10 km and the sort e5
#You have to get the key from https://creativecommons.tankerkoenig.de/ and add it to the following url, change xxxx to the key
url = "https://creativecommons.tankerkoenig.de/json/list.php?lat=47.6420482&lng=8.0756351&rad=10&sort=price&type=e5&apikey=xxxx"
#get the data from the API in json   
data = requests.get(url).json()
get_stations= data["stations"]


       
#define a for loop to get the names and the prices of the gas stations near my location
#https://stackoverflow.com/questions/5320871/in-list-of-dicts-find-min-value-of-a-common-dict-field
for items in get_stations:
    min_price= min(get_stations, key=lambda x:x["price"])
name = min_price["name"]
price = min_price["price"]
distance = min_price["dist"]

#part2: sending the mail
# set the text I want to send in the mail later
text = "Der Preis von " + str(price) + " €" + " der Tankstelle " + name  + " ist am günstigsten." + " Die Tankstelle ist " + str(distance) + " km entfehrnt."

#Change the Subject of the mail if the gas price is under 1.200€
if price < 1.200:
    subject = "Der Tankpreis liegt unter 1.200"
else:
    subject= "Aktuell niedrigster Tankpreis"

#use a html content to sent a symbol within the mail
#I added a gas station symbol from https://images-na.ssl-images-amazon.com/images/I/51hxhlP-UDL.png
html= """<img alt="Billiger Tanken" class="n3VNCb"
src="https://images-na.ssl-images-amazon.com/images/I/51hxhlP-UDL.png"
data-deferred="1" id="imi" data-w="512" data-h="512" jsname="HiaYvf"
jsaction="load:XAeZkd;" data-atf="true" data-iml="7733.460000003106"
style="height: 50px; width: 50px; margin: 0px;">"""    

#set the sender and reciver mail, the reciver dont have to be a gmail
sender_email = "your@gmail.com"
receiver_email = "any@gmail.com"

#create a txt file with the password and open it

datei = open("passwort.txt", "r")
password = datei.readline()


# Create a the message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  

# Add body to email

message.attach(MIMEText(text, "plain"))
message.attach(MIMEText(html, "html"))


# Log in to server using secure context and send email

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail("your@gmail.com", "any@gmail.com", message.as_string())
    server.quit()

