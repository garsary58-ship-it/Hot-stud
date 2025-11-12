import aiogram
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup
import pdfkit
import os
API_TOKEN = os.environ['API_TOKEN']
STUDOCU_USERNAME = os.environ['STUDOCU_USERNAME']
STUDOCU_PASSWORD = os.environ['STUDOCU_PASSWORD']
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! Send me a Studocu link to download the PDF file.")
@dp.message_handler()
async def handle_link(message: types.Message):
    link = message.text
    if 'studocu.com' in link:
        try:
            # Send a message to the user to wait
            await message.reply("Downloading PDF file...")
            # Login to Studocu using your premium account credentials
            session = requests.Session()
            login_url = 'https://www.studocu.com/login'
            login_data = {
                'username': STUDOCU_USERNAME,
                'password': STUDOCU_PASSWORD
            }
            session.post(login_url, data=login_data)
            # Get the PDF file link
            response = session.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            pdf_link = None
            for a in soup.find_all('a', href=True):
                if a['href'].endswith('.pdf'):
                    pdf_link = 'https://www.studocu.com' + a['href']
                    break
            # Download the PDF file
            if pdf_link:
                pdf_response = session.get(pdf_link)
                with open('document.pdf', 'wb') as file:
                    file.write(pdf_response.content)
                # Send the PDF file to the user
                with open('document.pdf', 'rb') as file:
                    await message.reply_document(file)
            else:
                await message.reply("PDF file not found.")
        except Exception as e:
            await message.reply("Error downloading PDF file: " + str(e))
    else:
        await message.reply("Please send a valid Studocu link.")
if _name_ == '_main_':
    executor.start_polling(dp, skip_updates=True)
