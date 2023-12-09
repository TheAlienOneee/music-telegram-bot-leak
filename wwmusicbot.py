import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
import yt_dlp
import os
import time

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6763542910:AAGogimj8NK7JAqu7t4oofJFr4qg5xXNqbk")
dp = Dispatcher(bot)

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
	def __init__(self):
		super(FilenameCollectorPP, self).__init__(None)
		self.filenames = []

	def run(self, information):
		self.filenames.append(information["filepath"])
		return [], information

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply("\U0001F44B Приветствую тебя, пользователь!\U0001F44B\n\U0001F3B6 Данный бот умеет проигрывать музыку.\nНапиши название песни и ты сможешь слушать её прямо в Telegram или скачать её и слушать где угодно!\n\U0001F6E0 (через '/'play название) \U0001F6E0")

@dp.message_handler(commands=['play'])
async def search(message: types.Message):
	arg = message.get_args()
	await message.reply('Загрузка...')
	YDL_OPTIONS = {'format': 'bestaudio/best',
		'noplaylist':'True',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '320'
		}],
	}

	with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
		try:
			get(arg) 
		except:
			filename_collector = FilenameCollectorPP()
			ydl.add_post_processor(filename_collector)
			video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
			await message.reply_document(open(filename_collector.filenames[0], 'rb'))
			await message.reply('Файл был отправлен!')
			time.sleep(5)
			os.remove(filename_collector.filenames[0])

		else:
			video = ydl.extract_info(arg, download=True)

		return filename_collector.filenames[0]

@dp.message_handler(commands=['yt'])
async def youtube(message: types.Message):
	arguments = message.get_args()
	await message.reply("Ожидайте...")
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '320',
		}],
	}
	
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		filename_collector = FilenameCollectorPP()
		ydl.add_post_processor(filename_collector)
		ydl.download([arguments])
		await message.reply_document(open(filename_collector.filenames[0], 'rb'))
		await message.reply('Файл был отправлен!')
		time.sleep(5)
		os.remove(filename_collector.filenames[0])
		return filename_collector.filenames[0]
	
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
