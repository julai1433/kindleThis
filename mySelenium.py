from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import pathlib
import os

DOWNLOADS_PATH = os.environ.get('local_library_path')

def CallBrowser(url, logger=None):
    print('Configuring Firefox...')
    firefox_options = webdriver.FirefoxOptions()

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('browser.download.folderList', 2)
    firefox_profile.set_preference('browser.download.dir', str(pathlib.Path(DOWNLOADS_PATH).absolute()))
    firefox_profile.set_preference('browser.cache.disk.enable', False)
    firefox_profile.set_preference('browser.cache.memory.enable', False)
    firefox_profile.set_preference('browser.cache.offline.enable', False)
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.helperApps.neverAsk.openFile","aapplication/octet-stream");
    firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False);
    firefox_profile.set_preference("browser.download.manager.useWindow", False);
    firefox_profile.set_preference("browser.download.manager.focusWhenStarting", False);
    firefox_profile.set_preference("browser.download.manager.showAlertOnComplete", False);
    firefox_profile.set_preference("browser.download.manager.closeWhenDone", True);

    # Set up Firefox options with the configured profile    
    firefox_options.profile = firefox_profile
    firefox_options.headless = False
    firefox_options.add_argument('--private')
    
    
    if logger != None:
        logger.info('CARGANDO NAVEGADOR ...')
    else:
        print("\nCARGANDO NAVEGADOR ...\n")
    global driver
    driver = webdriver.Firefox(options=firefox_options)

    driver.get(url)
def CloseBrowser():
    driver.quit()
def FindElementByPartialLinkText(text):
    return driver.find_element(By.PARTIAL_LINK_TEXT, text)
def FindElementByPath(text):
    return driver.find_element(By.XPATH, text)
def FindElementsByLinkText(text):
    return driver.find_elements(By.LINK_TEXT, text)
def FindElementsByClass(text):
    return driver.find_elements(By.CLASS_NAME, text)


def FillBlank(id, dato):
    responsiveField = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, id))
    )    
    responsiveField.clear()
    responsiveField.send_keys(dato)
    time.sleep(1)
def FillBlankByPath(path, dato):
    responsiveField = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, path))
    )    
    responsiveField.clear()
    responsiveField.send_keys(dato)
    responsiveField.send_keys(Keys.ENTER)
def FillBlankByName(name, dato):
    responsiveField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, name))
    )    
    responsiveField.clear()
    responsiveField.send_keys(dato)
    time.sleep(1)
def FillBlankById(id, dato):
    responsiveField = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, id))
    )    
    responsiveField.clear()
    responsiveField.send_keys(dato)
    time.sleep(1)
def FillBlankByClass(class_name, dato):
    responsiveField = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )    
    responsiveField.clear()
    responsiveField.send_keys(dato)
    time.sleep(1)

def ClickByPath(path):
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, path))
    )    
    element.click()
def ClickById(id):
    cli = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, id))
    )  
    cli.click()
def ClickByName(name):
    cli = driver.find_element(By.NAME, name)
    cli.click()
def ClickByPartialLinkText(text):
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, text))
    )    
    element.click()
def ClickByLinkText(text):
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, text))
    )    
    element.click()
def ClickByClass(class_name):
    cli = driver.find_element(By.CLASS_NAME, class_name)
    driver.execute_script("arguments[0].scrollIntoView();", cli)
    cli.click()
def ClickLocation(location, element = None):
    # Create an action chain
    actions = ActionChains(driver)
    # Scroll to the location of the element
    driver.execute_script(f"window.scrollTo({location['x']}, {location['y'] - 50})")
    if element != None:
        actions.move_to_element(element).perform()
    # Move to the location and click
    actions.move_by_offset(location['x'], location['y']).click().perform()

def ClickOneOfVariousByPartialLinkText(text, element = 0):
    time.sleep(2)
    elements = driver.find_elements(By.PARTIAL_LINK_TEXT, text)
    e = elements[element]
    e.click()

def ClickIfExistsByPath(xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
        if element.is_displayed() and element.is_enabled():
            ClickByPath(xpath)
    except:
        #Element not found, I'll move on with my life
        pass

def CheckExistsById(id):
    try:
        driver.find_element(By.ID, id)
    except NoSuchElementException:
        return False
    return True
def CheckExistsByClass(class_name):
    try:
        driver.find_element(By.CLASS_NAME, class_name)
    except NoSuchElementException:
        return False
    return True
def CheckExistsByXpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True
def CheckExistsByPartialLinkText(text):
    try:
        driver.find_element(By.PARTIAL_LINK_TEXT, text)
    except NoSuchElementException:
        return False
    return True
def CheckExistsByLinkText(text):
    try:
        driver.find_element(By.LINK_TEXT, text)
    except NoSuchElementException:
        return False
    return True
def CheckExistsAndIsClickableByXpath(xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
        return element.is_displayed() and element.is_enabled()
    except Exception:
        return False

def GetLocationById(id):
    e = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, id))
    )
    return e.location

def GetElementById(id):
    e = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, id))
    )
    return e

def CheckboxCheckById(id):
    cb = GetElementById(id)
    cb.send_keys(Keys.SPACE)

def ComboBoxSelectValueById(id, value):
    # Find the combo box element
    combo_box = Select(GetElementById(id))
    # Select an option by visible text
    combo_box.select_by_visible_text(value)

def WaitTilIsClickableById(id):
    # Wait for the element to be clickable
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, id)))

def GetInnerTextByClass(class_name):
    element = driver.find_element(By.CLASS_NAME, class_name)
    inner_text = element.text
    return inner_text

def GoToLastTab():

    # Get the handles of all open tabs
    all_tabs = driver.window_handles
    # Switch to the new tab (it might be the last one in the list)
    new_tab = all_tabs[-1]
    driver.switch_to.window(new_tab)

def GetDownLoadedFileName(waitTime):
    driver.execute_script("window.open()")
    WebDriverWait(driver,10).until(EC.new_window_is_opened)
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("about:downloads")

    endTime = time.time()+waitTime
    while True:
        try:
            fileName = driver.execute_script("return document.querySelector('#contentAreaDownloadsView .downloadMainArea .downloadContainer description:nth-of-type(1)').value")
            if fileName:
                return fileName
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break
