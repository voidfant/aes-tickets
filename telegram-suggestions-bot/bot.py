import aiogram.utils.executor
import logging
from create_bot import dp
from handlers import main_handler

logging.basicConfig(level=logging.INFO)

main_handler.setup_dispatcher(dp)

if __name__ == "__main__":
    aiogram.utils.executor.start_polling(dp)
