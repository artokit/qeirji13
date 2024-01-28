from aiogram import Dispatcher, Bot
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from routers import user, admin


async def run():
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot('6460562167:AAGJZkEOr1-2yJ0cAL6Hc2xpqTnF55he1bw')
    dp.include_routers(user.router, admin.router)
    await dp.start_polling(bot, skip_updates=True)


asyncio.run(run())
