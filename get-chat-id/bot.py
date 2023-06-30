import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging.basicConfig(level=logging.INFO)

API_TOKEN = "6144639378:AAE6fSifE07tmLIdr683gpXiPWT7Az1J36A"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands="get_id")
async def get_id_dammit(message: types.Message):
    # await message.reply(f"Базар, держи: {message.as_json}")
    logging.log(logging.INFO, [message.message_thread_id, message.chat.id])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
