from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time



def change_password(ip):
    """ Checnge Password bdcom onu """
    #Url login path
    url = f'http://{ip}/admin/login.asp'
    
    #Get firefox useragent
    USERAGENT = UserAgent().firefox

    # Options for the Firefox driver set useragemt
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", USERAGENT)

    # Webdriver useragent options
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(url=url)
        time.sleep(2)
        
        # Username input
        login_input = driver.find_element(By.NAME, 'username')
        login_input.clear()
        login_input.send_keys('admin')
        
        # Password input
        password_input = driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys('123456789')
        time.sleep(1)
        
        # Login
        login_submit = driver.find_element(By.NAME, 'save').click()  # Use click() to click the element

        
        #Password change
        driver.get(f'http://{ip}/password.asp')
        time.sleep(5)
        
        #oldpassword set
        old_pass_input = driver.find_element(By.NAME, 'oldpass')
        old_pass_input.clear()
        old_pass_input.send_keys('123456789')
        
        #newpassword set
        new_pass_input = driver.find_element(By.NAME, 'newpass')
        new_pass_input.clear()
        new_pass_input.send_keys('123456')

        #confirmed password
        conf_pass_input = driver.find_element(By.NAME, 'confpass')
        conf_pass_input.clear()
        conf_pass_input.send_keys('123456')

        #apply changes
        apply_change = driver.find_element(By.NAME, 'save').click()

        time.sleep(30)
    except Exception as error:
        print(error)

    finally:
        driver.close()
        driver.quit()
    
def mass_pass_change(ip_file):
    """ Changin password with based ip list """
    
    #Handle unicode format and file not found error
    try:
        with open(ip_file, 'r', encoding="utf-8") as file:
            ip_list = file.readlines()
    except FileNotFoundError: 
        print('[*] File not found [*]')
    except UnicodeError:
        print('[*] Working only UTF-8 files [*]')


    #iter on ip lists and change massive ONU password
    for ip in ip_list:
        #Get string ip end extract new line
        ip = str(ip.split('\n'))
            
        #Call change ip change function and change all list ONU password
        change_password(ip)

def main():
    try:
        mass_pass_change()
    except KeyboardInterrupt:
        print('[*] User stoped program [*]')

#Call function
main()