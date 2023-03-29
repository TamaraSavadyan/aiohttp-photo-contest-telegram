import typing
from logging import getLogger
import logging
from aiogram import Bot, Dispatcher, executor, types
from app.store.telegram_api.dataclasses import Message, Update

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(
        self, app: "Application", bot: "Bot", dispatcher: "Dispatcher"
    ):
        self.app = app
        self.bot = bot
        self.dispatcher = dispatcher
        self.logger = getLogger("handler")

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            await self.app.store.telegram_api.send_message(
                Message(
                    user_id=update.object.user_id,
                    text=self.bot.message.text,
                )
            )


API_TOKEN = "6296080745:AAHFohTB5Yi-4uFQoLp0Gd4LWY9kgz0SzP8"


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: types.Message):
#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


executor.start_polling(dp, skip_updates=True)
