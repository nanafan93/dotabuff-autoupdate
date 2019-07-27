#Handle SMTP 
import os
import smtplib
from email.message import EmailMessage
#Handle Scraping and Tabulation
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
#Windows Toast Notifications
from win10toast import ToastNotifier
#Time delay for requests ?
import time
toaster = ToastNotifier()

final_data = []

email = os.environ.get('EMAIL_ADDRESS')
pwd = os.environ.get('GMAIL_PYTHON_APP-PWD')
target = ['shubhankarranade30@gmail.com','shibbugokhale@gmail.com','hlim0019@student.monash.edu']
msg = EmailMessage()
msg['Subject'] = 'Dotabuff Update'
msg['From'] = email
msg['To'] = target

header = {'Origin': 'https://dotabuff.com',
          'Referer': 'https://www.dotabuff.com/players/120893135',
          'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

r = requests.get('https://www.dotabuff.com/players/120893135', headers=header)
pageSoup = soup(r.text, 'html.parser')
games = pageSoup.find('div', 'r-table r-only-mobile-5 performances-overview')
games = games.find('div', 'r-row')
body = games.find_all('div', 'r-body')
hero = body[0].a.next_element.next_element.text
result = body[1].a.text
duration = body[3].text
kda = body[4].text
gameDict = {'Hero': hero, 'Result': result, 'Duration': duration, 'KDA': kda}
final_data.append(gameDict)
final_data = pd.DataFrame(final_data)
old_data = pd.read_csv('D:\Dotabuff.csv',index_col = 0)
old_data = pd.DataFrame(old_data)
if(old_data.equals(final_data)):
    if(final_data['Hero'].equals(old_data['Hero']) and final_data['KDA'].equals(old_data['KDA']) and final_data['Duration'].equals(old_data['Duration'])):
        toaster.show_toast('Dotabuff Update','No New Games Played')
        msg.set_content('No New Games Played')  
else:
    if(result=='Lost Match' or result=='Abandoned'):
        if(result=='Lost Match'):
            toaster.show_toast('Dotabuff Update','Heavy Losses by Harshu\nHero: %s\nKDA: %s\nDuration: %s'%(hero,kda,duration))
            content_loss ='Heavy Losses by Harshu\nHero: %s\nKDA: %s\nDuration: %s'%(hero,kda,duration)
            msg.set_content(content_loss)
        else:
            toaster.show_toast('Dotabuff Update','ABANDON ALERT ! LMAO\nHero: %s\nKDA: %s\nDuration: %s'%(hero,kda,duration))
            content_abandon = 'ABANDON ALERT ! LMAO\nHero: %s\nKDA: %s\nDuration: %s'%(hero,kda,duration)
            msg.set_content(content_abandon)
       
    else:
        toaster.show_toast('Dotabuff Update','Epic Win') 
final_data = pd.DataFrame(final_data)
final_data.to_csv('D:/DotaBuff.csv', index='False')
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email,pwd)
    smtp.send_message(msg)