from lxml import html
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import secmail

client = secmail.Client()

emails = client.random_email(amount=1, domain="1secmail.net")

driver = webdriver.Firefox()
driver.implicitly_wait(30)

driver.get("https://signup.live.com/signup")

email_input = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "MemberName"))
)

next_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "iSignupAction"))
)

email_input.send_keys(emails[0])
next_button.click()

password_input = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "PasswordInput"))
)

password_input.send_keys("w3KuNk8Z6wc0T8I1iyhx")

next_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "iSignupAction"))
)
next_button.click()

first_name_input = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "FirstName"))
)

last_name_input = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "LastName"))
)

first_name_input.send_keys("None")
last_name_input.send_keys("None")

next_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "iSignupAction"))
)
next_button.click()

birth_month_input = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "BirthMonth"))
)

Select(birth_month_input).select_by_value("1")

birth_day_input = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "BirthDay"))
)

Select(birth_day_input).select_by_value("1")

birth_year_input = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "BirthYear"))
)

birth_year_input.send_keys("1984")

next_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "iSignupAction"))
)

next_button.click()

code_input = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "VerificationCode"))
)

### NOW CHECK MAIL
email_body = None
max_retries = 10
retries = 0
while True:
    inbox = client.get_inbox(emails[0])
    print(f'Checking {emails[0]}')
    if len(inbox) > 0:
        #PARSE EMAIL
        for message in inbox:
            print(message)
            email_message = client.get_message(address=emails[0], message_id=message.id)
            email_body = email_message.body
        break
    
    if retries == max_retries:
        print("Failed to receive email")
        exit()
    
    retries += 1
    time.sleep(5)
    
tree = html.fromstring(email_body)

code_xpath = "//span[contains(@style, 'Segoe UI Bold')]"

code_element = tree.xpath(code_xpath)
if code_element:
    security_code = code_element[0].text
    print(f"Security Code: {security_code}")
else:
    print("Security code not found.")
    exit()
    
    
code_input.send_keys(security_code)

next_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "iSignupAction"))
)

next_button.click()

# NOW AT CAPTCHA :(