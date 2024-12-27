from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import sys
import time
import argparse


def change_password(ip):
    """ Checnge Password bdcom onu """
    
    #Get oldpasswrd and new password
    current_password = input('Enter current password: ')
    new_password = input('Enter new password: ')
    if len(new_password) > 0 and len(new_password) > 20:
        print('[*] You can set password 1-20 ascii character [*]')
        sys.exit()
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
        password_input.send_keys(current_password)
        time.sleep(1)
        
        # Login
        login_submit = driver.find_element(By.NAME, 'save').click()  # Use click() to click the element

        
        #Password change
        driver.get(f'http://{ip}/password.asp')
        time.sleep(5)
        
        #oldpassword set
        old_pass_input = driver.find_element(By.NAME, 'oldpass')
        old_pass_input.clear()
        old_pass_input.send_keys(current_password)
        
        #newpassword set
        new_pass_input = driver.find_element(By.NAME, 'newpass')
        new_pass_input.clear()
        new_pass_input.send_keys(new_password)

        #confirmed password
        conf_pass_input = driver.find_element(By.NAME, 'confpass')
        conf_pass_input.clear()
        conf_pass_input.send_keys(new_password)

        #apply changes
        apply_change = driver.find_element(By.NAME, 'save').click()

        time.sleep(1)
    except Exception as error:
        print(error)
    finally:
        driver.close()
        driver.quit()
        sys.exit()
    
def mass_pass_change(ip_file):
    """ Changin password with based ip list """
    
    #Handle unicode format and file not found error
    try:
        with open(ip_file, 'r', encoding="utf-8") as file:
            ip_list = file.readlines()
    except FileNotFoundError: 
        print('[*] File not found [*]')
        sys.exit()
    except FileExistsError:
        print('[*] File not exist [*]')
        sys.exit()
    except (UnicodeEncodeError, UnicodeError, UnicodeDecodeError):
        print('[*] Working only UTF-8 files [*]')
        sys.exit()


    #iter on ip lists and change massive ONU password
    for ip in ip_list:
        #Get string ip end extract new line
        ip = ip.strip()
        
        #Call change ip change function and change all list ONU password
        change_password(ip)


#Call functions
def main():
    #Argument handle
    parser = argparse.ArgumentParser(description='This tool help yout change massive BDcom ONU passwords')
    parser.add_argument('-f', '--file', type=str, help='Ip list file path')

    #Chek argements provided by user
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()
    

    try:
        if args.file:
            mass_pass_change(args.file)
    except KeyboardInterrupt:
        print('[*] User stoped program [*]')
        sys.exit()


#Call function
if __name__ == '__main__':
    main()
