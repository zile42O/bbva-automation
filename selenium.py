from selenium import webdriver
import undetected_chromedriver as uc

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import re
import sys
import time
import sys
import requests
import base64
from faker import Faker

START_URL = "https://httpbin.org/ip" # for checking proxy
WORK_URL = "https://web.bbva.it/public.html#signup"

BOT_CHAT = "1542585085"
BOT_TOKEN = "6932991030:AAF2mD4ATfXLd2QIstFn4ln2DV6lOJazwcM"
NUMBERS_FILE = 'numbers.txt'

faker = Faker()

def setup_proxy(user: str, password: str, endpoint: str) -> dict:
	wire_options = {
		"proxy": {
			"http": f"http://{user}:{password}@{endpoint}",
			"https": f"http://{user}:{password}@{endpoint}",
			'no_proxy': 'localhost,127.0.0.1'

		}
	}
	return wire_options

def process_number(number, numbers_list):
	#USERNAME = ""
	#PASSWORD = ""
	#ENDPOINT = ""
	#proxies = setup_proxy(USERNAME, PASSWORD, ENDPOINT)
	
	chrome_options = uc.ChromeOptions()
	chrome_options.add_argument('--ignore-certificate-errors')

	#driver = uc.Chrome(options=chrome_options, seleniumwire_options=proxies)
	driver = uc.Chrome(options=chrome_options)

	fake_first_name = faker.first_name()
	fake_last_name = faker.last_name()
	fake_email = faker.email()

	try:
		driver.get(START_URL)
		driver.execute_script('return navigator.webdriver')
		driver.implicitly_wait(30)
		time.sleep(5)
		driver.get(WORK_URL)

		element = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.ID, 'input-name'))
		)

		element.send_keys(fake_first_name)
		time.sleep(1)
		element = driver.find_element(By.ID, 'input-lastName')
		element.send_keys(fake_last_name)
		time.sleep(1)
		element = driver.find_element(By.ID, 'input-telephone')
		element.clear()
		number_without_prefix = number[2:]
		element.send_keys(number_without_prefix)
		time.sleep(1)
		element = driver.find_element(By.ID, 'input-confirmTelephone')
		element.clear()
		number_without_prefix = number[2:]
		element.send_keys(number_without_prefix)
		time.sleep(1)
		element = driver.find_element(By.ID, 'input-email')
		element.send_keys(fake_email)
		time.sleep(1)
		element = driver.find_element(By.XPATH, '/html/body/philip-public-app-view/div/div/main/div/div/component-anchor/multistep-component-fullscreen/div/div[2]/div/div/div/form/div/component-anchor/div[3]/haunted-checkbox/label/span')
		element.click()

		cookies = driver.get_cookies()

		for cookie in cookies:
			print(cookie)

		time.sleep(5)

		element = driver.find_element(By.ID, 'multistep-next-button')
		element.click()

		## Informazioni aggiuntive
		time.sleep(5)

		element = driver.find_element(By.ID, 'input-birthDate_day')
		element.send_keys("14")

		element = driver.find_element(By.ID, 'input-birthDate_month')
		element.send_keys("12")

		element = driver.find_element(By.ID, 'input-birthDate_year')
		element.send_keys("1998")

		# Prov

		element = driver.find_element(By.ID, "input-onboarding-province-predictive")
		element.send_keys("FERM")
		time.sleep(1)
		first_option_xpath = "//*[contains(text(), 'FERMO')]"
		first_option = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, first_option_xpath))
		)
		actions = ActionChains(driver)
		actions.move_to_element(first_option).click().perform()
		time.sleep(5)

		element = driver.find_element(By.ID, "input-onboarding-municipality-predictive")
		element.send_keys("FERM")
		time.sleep(1)
		first_option_xpath = "//*[contains(text(), 'FERMO')]"
		first_option = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, first_option_xpath))
		)
		actions = ActionChains(driver)
		actions.move_to_element(first_option).click().perform()

		# Sex
		element = driver.find_element(By.XPATH, '/html/body/philip-public-app-view/div/div/main/div/div/component-anchor/multistep-component-fullscreen/div/div[2]/div/div[2]/div/form/div/component-anchor/haunted-radio-group/fieldset/div[1]/haunted-radio-input[1]/label')

		element.click()

		# Next button
		element = driver.find_element(By.ID, 'multistep-next-button')
		element.click()
		#
		time.sleep(9999) 

		# todo 3d page

	finally:
		driver.quit()
		#numbers_list.remove(number) #uncomment at finish

with open(NUMBERS_FILE, 'r') as file:
	numbers = file.read().splitlines()
	numbers_copy = numbers.copy()
	for number in numbers_copy:
		process_number(number, numbers)
		time.sleep(2)

with open(NUMBERS_FILE, 'w') as file:
	file.write('\n'.join(numbers))