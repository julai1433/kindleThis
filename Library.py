# Process:
# - search for a book on a list of websites and download it.    SEARCH & DOWNLOAD.
# - upload it to bionic reading and download it again.          BIONIC.
# - rename it and send it to the kindle through email.          SEND TO KINDLE.
# 
#

import mySelenium as mS
import time
import os
import shutil
import logging
import sys
from urllib import request, parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from unidecode import unidecode
from decouple import AutoConfig
config = AutoConfig('.env')


LIBRARY = config('local_library_path')
BOOKS_SUPPLIER = "https://ww3.lectulandia.com/"
BIONIC_SITE = "https://app.bionic-reading.com/"

EMAIL_ADDR = config('sender_email_addr')
EMAIL_PSWD = config('sender_email_pswd')
KINDLE_EMAIL = config('my_kindle_email')

HEADLESS_MODE = config('silent_mode')


# - SEARCH & DOWNLOAD.
#     - Description: Searches and downloads an ebook on a website and stores it in the library.
#     - Input: Tuple with two Strings (book's name and author)
#     - Output: Boolean True if succeded on the task, False elseway
def searchAndDownload(book_data, silent_mode=HEADLESS_MODE):
#     - Steps:
#         - Go to the source of ebooks to find the book.
#         - First looking for ebooks, then for PDFs.
#         - If it is found, download it to the library.
    book_name = book_data[0]
    book_author = book_data[1]
    try:
        print("Searching \""+book_name+"\" from "+book_author+" ...")
        if os.path.exists(LIBRARY+'/'+book_name+'/'+book_name+'.epub'):
            print("Book was already in your library")
            return True
        output = False
        mS.CallBrowser(BOOKS_SUPPLIER, silent_mode=silent_mode)
        mS.ClickByClass("formWrapper")
        #book_data_seek = book_name+" "+book_author if book_author != "AUTHOR UNKNOWN" else book_name
        book_data_seek = book_name
        mS.FillBlankByPath("/html/body/div/header/nav/ul/li[4]/form/input", book_data_seek)
        cond=True
        waitTime = 180
        endTime = time.time()+waitTime
        while(cond):
            try:
                titles = mS.FindElementsByClass("page-title")
                if len(titles) < 2:
                    cond = False
            except:
                pass
            time.sleep(1)
            if time.time() > endTime:
                break
        if not cond:
            results = mS.FindElementsByClass("card")
            if len(results):
                for result in results:
                    book_author_str = book_author if book_author != "AUTHOR UNKNOWN" else book_name
                    if book_name in result.text and book_author_str in result.text:
                        result.click()
                        mS.ClickById("download1")
                        mS.GoToLastTab()
                        time.sleep(6)
                        mS.ClickById("downloadB")
                        os.makedirs(LIBRARY+'/'+book_name, exist_ok=True)
                        print("Downloading ...")
                        file_name = mS.GetDownLoadedFileName(180)
                        print("Downloaded as: "+file_name)
                        shutil.move(LIBRARY+'/'+file_name, LIBRARY+'/'+book_name+'/'+book_name+'.epub')
                        output = True
                        break
            else:
                print("Not found")
        print("Closing Browser")
        mS.CloseBrowser()
        return output
    except Exception as e:
        print(e)
        return False
    
# - BIONIC.
#     - Description: Takes an ebook file from the library and replaces it for a version with bionic reading font.
#     - Input: None
#     - Output: Boolean True if succeded on the task, False elseway
def bionicBook(book_name):
#     - Steps:
#         - Open the bionic reading site
#         - Load the ebook file
#         - Once it's done, download the new ebook file to the library.
#         - Rename it with the actual name.
    print("Processing the book with Bionic Reading ...")
    if os.path.exists(LIBRARY+'/'+book_name+'/'+book_name+'-br.epub'):
        print("Book was already in your Bionic Reading library")
        return True
    output = False
    mS.CallBrowser(BIONIC_SITE)
    try:
        if mS.CheckExistsAndIsClickableByXpath("/html/body/div[2]/div[3]/div/div/button[1]"):
            mS.ClickByPath("/html/body/div[2]/div[3]/div/div/button[1]")
        else:
            mS.ClickByPath("/html/body/div[3]/div[3]/div/h2/button")
            time.sleep(1)
            mS.ClickByPath("/html/body/div[2]/div[3]/div/div/button[1]")
        time.sleep(1)
        mS.ClickIfExistsByPath("/html/body/div[2]/div[3]/div/h2/button")
        mS.ClickById("content-tab-2")
        # mS.ClickByPath("/html/body/div/div[1]/div[2]/div/div/div/div/button")
        inputFile = mS.FindElementByPath("/html/body/div/div[1]/div[2]/div/div/div/div/input")
        inputFile.send_keys(LIBRARY+'/'+book_name+'/'+book_name+'.epub')
        mS.ClickByPath("/html/body/div/div[1]/header/div/div/div[2]/div/button")                #Process
        mS.ClickByPath("/html/body/div[2]/div[3]/div/div/div/label/span[1]/span[1]/input")      #Accept License Agreement
        mS.ClickByPath("/html/body/div[2]/div[3]/div/div/button")                               #Continue
        cond=True
        waitTime = 180
        endTime = time.time()+waitTime
        while(cond):
            try:
                if mS.CheckExistsByXpath("/html/body/div/div[2]/header/div/div/div/div[2]/button[2]"):
                    cond = False
                elif mS.CheckExistsByXpath("/html/body/div[2]/div[3]/div/div/div[2]/button[2]"):
                    break
            except:
                pass
            time.sleep(1)
            if time.time() > endTime:
                break
        if not cond:
            mS.ClickByPath("/html/body/div/div[2]/header/div/div/div/div[2]/button[2]")
            mS.ClickByPath("/html/body/div[2]/div[3]/div/div/ul/div[2]")

            cond=True
            waitTime = 180
            endTime = time.time()+waitTime
            while(cond):
                try:
                    if mS.CheckExistsByXpath("/html/body/div[2]/div[3]/div/div/button"):
                        cond = False
                except:
                    pass
                time.sleep(1)
                if time.time() > endTime:
                    break
            if not cond:
                mS.ClickByPath("/html/body/div[2]/div[3]/div/div/button")
                # mS.ClickByPath("/html/body/div[2]/div[3]/div/div/button")
                file_name = mS.GetDownLoadedFileName(180)
                shutil.move(LIBRARY+'/'+file_name, LIBRARY+'/'+book_name+'/'+book_name+'-br'+'.epub')
                print("Done!")
                output = True
            else:
                print("Failed while converting")
        else:
            print("Failed while uploading file to BR")
    except:
        print("something went wrong")
    finally:
        print("Closing browser")
        mS.CloseBrowser()
    return output


# - SEND TO KINDLE.
#     - Description: Takes an ebook file from the library and sends it through email to your kindle.
#     - Input: String book's name
#     - Output: Boolean True if succeded on the task, False elseway
def sendToKindle(book_name, kindle_address = KINDLE_EMAIL):
#     - Steps:
#         - Checks the book is in the library, returns error if not, 
#         - Sends the email with the book file attached.

    # Your email address and credentials
    sender_email = EMAIL_ADDR
    sender_password = EMAIL_PSWD

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = kindle_address
    message["Subject"] = f"Send to Kindle: {book_name}"

    # Attach the ebook file
    
    file_path = LIBRARY+f"/{book_name}/{book_name}.epub"
    download_name = book_name

    file_path_bionic = LIBRARY+f"/{book_name}/{book_name}-br.epub"
    if os.path.exists(file_path_bionic):
        file_path = file_path_bionic
        download_name = book_name + '-br'

    with open(file_path, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {unidecode(download_name)}.epub")
        message.attach(part)

    # Connect to the SMTP server and send the email
    try:
        print("Sending email ...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, kindle_address, message.as_string())
        print("Email sent successfully.")
        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False

# - GET BOOK NAME.
#     - Description: Takes the book name form the argument if any, if not; asks for it though the terminal.
#     - Input: None.
#     - Output: String book's name.
def getBookDataFromArgs():
    if len(sys.argv) > 1:
        book_name = sys.argv[1]
    else:
        book_name = input("Por eso joven, por eso, pero qué libro quieres pues? ...")
    if ',' in book_name:
        info = book_name.split(',')
    else:
        info = [book_name, "AUTHOR UNKNOWN"]
    info[0] = info[0].strip()
    info[1] = info[1].strip()
    return info

def getBookDataFromQuery(query):
    if ';' in query:
        info = query.split(';')
    else:
        info = [query, "AUTHOR UNKNOWN"]
    info[0] = info[0].strip()
    info[1] = info[1].strip()
    return info

# - IS BIONIC ENABLED.
#     - Description: Checks id the user wants to pass the book for the bionic_reading processing.
#     - Input: None.
#     - Output: Boolean True if the bionic_reading process is required, False elseway.
def isBionicEnabled():
    if len(sys.argv) > 2 and sys.argv[2] == "bionic":
        return True
    else:
        return False


if __name__ == '__main__':
    
    book_data = getBookDataFromArgs()
    book_name = book_data[0]


    try:
        if searchAndDownload(book_data):
            print("Book found and downloaded")
            if isBionicEnabled():
                try:
                    if bionicBook(book_name):
                        print("Book bionicled successfully")
                    else:
                        print("Bionicledization unsuccessful ):")
                except:
                    print("Bionicledization unsuccessful ):")
            try:
                if sendToKindle(book_name):
                    print("Book sent to Kindle")
                    print("Process finished correctly!")
                else:
                    print("Book not sent to Kindle")
            except:
                print("Book not sent to Kindle")
        else:
            print("Book not found")
    except:
        print("Process had some error, you should really consider a career change, maybe sell bonice or something")
    finally:
        print("Bye perro")
            
            
    



