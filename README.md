# kindleThis
Telegram Bot that helps you find/download/send ebooks to your kindle.

## Commands:

/start : Bot will give you the start message.

/set_kindle_email: Bot will ask you for the email you want to send the books.

/search : The bot will listen to your requested books.


## Features:

You can request any book, the bot will search for it and 
if it finds it, will download and send it to any email 
you set (normally you'd put your kindle account so you 
receive it directly to your kindle device)

## NOTES FOR THE USER:

### NOTE 1: 
Your amazon account won't let you receive ebooks from any unknown email account, so you have to go to your kindle preferences page and add this address as a trusted one:
"green.panda.3.1415@gmail.com"
I'll be using that address for now, let's see how that works.


### NOTE 2: 
When you request for any book, remember to separate the title from the author with a semicolon


## NOTES FOR THE DEV:

### Structure of the project:
    - Library/ : Directory where the downloaded books will be saved.
    - mySelenium.py : This is my personal library for Selenium, conatins several methods for scrapping.
    - Library.py : This is the library containing the methods for searching, download and send to kindle.
    - kindleThis.py : Main code for the Telegram Bot.

### To run it locally:
If you want to run this bot into your local environment:
- Create a file called .env
- Set the next variables:
    - kindle_this_token= The token for your Telegram bot (provided by the BotFather)
    - sender_email_addr= The email address you'll be sending the ebooks, in my case is "green.panda.3.1415@gmail.com"
    - sender_email_pswd= The password for the email
    - local_library_path= The absolut path to the Library directory, inn my case it is the project root + "/Library/"
- Install decouple and unicode with pip; individually or running pip install -r requirements.txt.










