# kindleThis
Telegram Bot that helps you send ebooks to your kindle.

Commands:
/start : Bot will give you the start message.
/set_kindle_email: Bot will ask you for the email you want to send the books you ask for.
/search : The bot will listen to your requested books.

Features:
You can request any book, the bot will search for it and 
if ti findws it, will download it and send it to any email 
you supply (normally you'd put your kindle account so you 
receive it directly to your kindle device)

NOTE 1: Your amazon account won't let you receive ebooks from 
any email account, so you have to go to your kindle preferences page and add this address as a trsuted one:
green.panda.3.1415@gmail.com
I'll be using that address for now, let's see how that works.

NOTE 2: When you request for any book, remember to separate 
the title from the author with a comma, if the title has a comma inside the title (I just realized that scenario is not 
beign covered so it probably will fail, or maybe it will download a different book from the one you wanted, I'll add it to the TO-DOs)



If you want to run this bot into your local environment:

- Create a file called .env
- Set the next variables:
    kindle_this_token= The token for your Telegram bot (provided by the BotFather)
    sender_email_addr= The email address you'll be sending the ebooks, in my case is "green.panda.3.1415@gmail.com"
    sender_email_pswd= The password for the email
    local_library_path= The absolut path to the Library directory, inn my case it is the project root + "/Library/"
- Install decouple and unicode with pip; individually or running pip install -r requirements.txt.
