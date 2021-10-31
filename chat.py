import requests as req
import time
import os
import database as db
import cryptocode as cc
from colorama import init,Fore, Back, Style
init()
logo = '______        _        _      _____  _             _   \n| ___ \\      (_)      | |    /  __ \\| |           | |  \n| |_/ /  ___  _   ___ | |__  | /  \\/| |__    __ _ | |_ \n|    /  / _ \\| | / __|| \'_ \\ | |    | \'_ \\  / _` || __|\n| |\\ \\ |  __/| || (__ | | | || \\__/\\| | | || (_| || |_ \n\\_| \\_| \\___||_| \\___||_| |_| \\____/|_| |_| \\__,_| \\__|\n\n\n'
user = db.database('user.db')
incomingM= []
cckey = "zxcSHITczSxc81"
server = 'http://WebJCou.pythonanywhere.com'

def send(to=None):
	os.system('clear')
	print(logo)
	msg_for = to
	if msg_for == None:
		msg_for = input(Fore.CYAN+'\n[$] Назад...\nСообщение для: '+Fore.RESET)
		if msg_for == '$':
			menu02()
		# нихуя я тут проверять не буду, если челик обосрется и отправит не тому - похуй, сервер удалит нахуй
	os.system('clear')
	print(logo)
	print(f"Сообщение для {msg_for}".center(25))
	text = input(Fore.CYAN+'\n[$] Назад...\nТекст: '+Fore.RESET)
	if msg_for == '$':
		menu02()
	if text == '$':
		menu02()
	# Ну а тут если все заебись хуярим запрос на сервак и отправляем эту ебалу
	r = req.post(f"{server}/send",json={'login':user.data['login'],'password':user.data['password'],'to':msg_for,'msg':cc.encrypt(text,cckey)}).json()

	menu02("Сообщение отправлено")
def drawMsg(msg):
	incomingM.remove(msg)
	os.system('clear')
	print(logo)
	r = req.post(f"{server}/read",json={'login':user.data['login'],'password':user.data['password'],'from':msg}).json()
	
	print(f"Сообщение от {r['from']}".center(25))



	print(f"\n\n{cc.decrypt(r['msg'],cckey)}\n\n[0] Назад...\n[1] Ответить")
	choise = input(Fore.CYAN+'\n\nВыбор: '+Fore.RESET)
	if choise == '0':
		incoming()
	elif choise == '1':
		send(msg)
	else:
		incoming()

def incoming():

	os.system('clear')
	print(logo)
	print(f"Входящие сообщения".center(25))
	print('\n\n   [0] В меню...\n_____________________________________\n')
	# тут херачим запрос на сервер ебаный, отправляем логин пароль, получаем сообщения.
	# for i in r.json():   Потом эту ебалу пиздошим в массив сообщений
	# 	incomingM.append(i)
	# for i in incomingM:         И потом всю эту ебалу из массива мы выводим нахуй
	# 	print(f'   [{indexOf(i)+1}] От {i['from']}\n')
	r = req.post(f"{server}/getlist",json={'login':user.data['login'],'password':user.data['password']}).json()
	for i in r:
		incomingM.append(i)

	for i in incomingM:         
		print(f'   [{incomingM.index(i)+1}] От {i}\n')

	choise = input(Fore.CYAN+'\n\nВыбор: '+Fore.RESET)
	if choise == '0':
		menu02()
	try:
		drawMsg(incomingM[int(choise)-1])
	except:
		incoming()

def menu02(msg=''):
	os.system('clear')
	print(logo)
	if msg!='':
		print(f"{msg}".center(25))
	print(f"Добро пожаловать, {user.data['login']}".center(25))
	print('\n\n   [1] Входящие сообщения\n   [2] Отправить сообщение')
	choise = input(Fore.CYAN+'\n\nВыбор: '+Fore.RESET)
	if choise == '1':
		incoming()
	elif choise=='2':
		send()
	else:
		menu02()

def register(msg=''):
	os.system('clear')
	print(logo)
	print("Регистрация".center(25))
	if msg!='':
		print(f"\n{msg}".center(25))
	login = input("\n\n"+Fore.CYAN+'Логин: '+Fore.RESET)
	os.system('clear')
	print(logo)
	print("Регистрация".center(25))
	password=input("\n\n"+Fore.CYAN+'Пароль: '+Fore.RESET)
	# Проверить данные и захуярить их в базу данных login password
	
	r = req.post(f"{server}/register",json={'login':login,'password':password}).json()
	if r['state']==False:
		register('Такой логин существует')
		

	# /\ ТУт должна быть првоерка данных через сервер, но сервера нет поэтмоу ебашу в холостную 
	user.add('login',login)
	user.add('password',password)

	menu02();

def enter(msg = ''):
	os.system('clear')
	print(logo)
	print("Вход".center(25))
	if msg!='':
		print(f"\n{msg}".center(25))
	login = input("\n\n"+Fore.CYAN+'Логин: '+Fore.RESET)
	os.system('clear')
	print(logo)
	print("Вход".center(25))
	password=input("\n\n"+Fore.CYAN+'Пароль: '+Fore.RESET)
	# Проверить данные и захуярить их в базу данных login password
	
	r = req.post(f"{server}/enter",json={'login':login,'password':password}).json()
	if 'state' in r:
		enter('Неверный логин и/или пароль')

	# /\ ТУт должна быть првоерка данных через сервер, но сервера нет поэтмоу ебашу в холостную 
	user.add('login',login)
	user.add('password',password)
	
	menu02();

def menu01():
	os.system('clear')
	print(logo)
	print('   [1] Вход\n   [2] Регистрация')
	choise = input(Fore.CYAN+'\n\nВыбор: '+Fore.RESET)
	if choise == '1':
		enter()
	elif choise=='2':
		register()
	else:
		menu01()

def main():
	if 'login' in user.data:
		menu02()
	else:
		menu01()
	
if __name__ == "__main__":
	os.system('clear')
	main()
