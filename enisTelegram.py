import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6133351339:AAFREw1oYXX_jBksoPLBIJVXGwrSaLimU2o")
dp = Dispatcher()

async def auth(message:types.Message):
    login = ""    
    password = ""
    parts = message.text.split()    
    for part in parts:
        if part.startswith("login:"):
            login = part.split("login:")[1]
        elif part.startswith("password:"):
            password = part.split("password:")[1]

    if not login or not password:
        await message.answer("Please provide both login and password.")
        return
    headers = {        
        "content-type":"application/json",
        "authorization":"Bearer null"
    }    
    payload = {        
        "login": login,
        "password": password,
        "captchaInput": ""
    }
    print()
    url = 'https://api.enis2.ml/login?city=tk'
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        await message.answer("Вход выполнен")
        userToken=response.json()['token']
    else:
        print(response)
        await message.answer("Хуй его знает ошибка какаято")
    return userToken
async def years(userToken):
    url='https://api.enis2.ml/dashboard/years?city=tk'
    headers={"Authorization": "Bearer "+userToken}
    response = requests.get(url, headers=headers).json()
    actual_year_id = None

    for item in response:
        if item["isActual"]:
            actual_year_id = item["Id"]
            break
    return actual_year_id

async def terms(userToken, year):
    url = f'https://api.enis2.ml/dashboard/terms/{year}?city=tk'
    headers = {"Authorization": "Bearer " + userToken}
    response = requests.get(url, headers=headers).json()
    print(response) 
    actual_term_id = None

    for item in response:
        if item["isActual"]:
            actual_term_id = item["Id"]
            break
    return actual_term_id


async def scores(userToken,term,message):
    url = f'https://api.enis2.ml/dashboard/diary/{term}?city=tk'
    headers = {"Authorization": "Bearer "+userToken}  
    print(headers)
    response = requests.get(url, headers=headers).json()
    print(response)
    
    data = response['data']
    print(data)
    message_text = ""
    for item in data:
        name = item['Name']
        score = item['Score']
        mark = item['Mark']
        message_text += f"{name}: {score}%,\nMark: {mark}\n"
    
    await message.answer(message_text)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello ma nigga akzhol")

@dp.message()
async def echo(message: types.Message):
    userToken=await auth(message)
    year=await years(userToken)
    term=await terms(userToken,year)

    #берем данные с уроков
    await scores(userToken,term,message)  

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())