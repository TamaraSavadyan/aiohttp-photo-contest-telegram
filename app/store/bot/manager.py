import logging
import asyncio
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Poll, PollType, ParseMode, ContentType
from config import configure
from database import DataBase
from utils import generate_tournament_bracket, compare_scores

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
TOKEN = configure.bot.token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# function to start bot


@dp.message_handler(commands=['start'])
async def start_command_handler(message: Message):
    await message.answer(
        text=md.text(
            md.bold('Hello!') + '\n\n'
            'Welcome to photo contest! '
            'Now you will be set to tournament bracket with other players. '
            'I will collect all the photos and create a contest for people to vote. '
            'The photo with the most votes wins!\n\n'
            'Good luck!\n\n'
            'Please wait 5 seconds before the tournament starts. '
        )
    )

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    score = 0
    profile_photo = await get_profile_picture(message)

    await DataBase.fill_users()
    await DataBase.add_user(user_id, first_name, last_name, score, profile_photo)
    await send_ticking_clock(message.from_user.id, 2)
    if not await DataBase.check_users_amount():
        await message.answer('Not enough players to start the tournament')
        return
    await send_tournament_bracket(user_id)


# function to stop bot
@dp.message_handler(commands=['stop'])
async def stop_command_handler(message: Message):
    await message.answer('Stopping the bot...')
    await bot.close()


# function to send ticking clock message
async def send_ticking_clock(user_id: int, duration: int):
    sent_message = await bot.send_message(chat_id=user_id, text='00:00')
    message_id = sent_message.message_id
    for i in range(duration, -1, -1):
        minutes, seconds = divmod(i, 60)
        time_str = f'{minutes:02d}:{seconds:02d}'
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=time_str)
        await asyncio.sleep(1)

    await bot.send_message(chat_id=user_id, text='Game started!')


# function to get profile picture
async def get_profile_picture(message: Message):
    # Get user profile photos
    photos = await bot.get_user_profile_photos(message.from_user.id)

    if len(photos.photos) > 0:
        profile_pic = photos.photos[0][-1].file_id
        return profile_pic


# function to send profile picture
@dp.message_handler(commands=['pic'])
async def send_picture_to_user(message: Message):
    user_id = message.from_user.id
    user = await DataBase.get_user(user_id)
    # Create a photo object
    photo = user.avatar_link
    # Send the photo to the user
    await bot.send_photo(chat_id=user_id, photo=photo)


# function to send tournament bracket
async def send_tournament_bracket(user_id: int):
    # Get the list of players
    players = await DataBase.get_users_names()
    # Generate the bracket
    text_bracket, bracket = generate_tournament_bracket(players)
    await DataBase.save_bracket(user_id, bracket)
    # Send the bracket to the user
    await bot.send_message(chat_id=user_id, text=f'Here is current tournament bracket:\n\n{text_bracket}')


async def create_poll(user_id: int):
    """Save the photos and create a poll for users to vote"""

    player1 = await DataBase.get_user(user_id)
    bracket = await DataBase.get_bracket(user_id)
    for tour in bracket:
        if player1 in tour:
            player2 = tour[0] if tour[1] == player1 else tour[1]
            break
    photo1 = player1.avatar_link
    photo2 = player2.avatar_link

    # Send a message with the two photos and a poll to vote for one or the other

    photo1_url = await bot.upload_photo(open(photo1, 'rb'))
    photo2_url = await bot.upload_photo(open(photo2, 'rb'))

    player1_text = f"{player1.first_name} {player1.last_name}"
    player2_text = f"{player2.first_name} {player2.last_name}"

    poll = Poll(
        question='Which picture do you like better?',
        options=[player1_text, player2_text],
        type=PollType.REGULAR,
        allows_multiple_answers=False
    )

    poll_message = await bot.send_poll(chat_id=user_id, question=poll.question, options=poll.options,
                                       type=poll.type, allows_multiple_answers=poll.allows_multiple_answers,
                                       is_anonymous=True, explanation="Please vote for your favorite picture!",
                                       explanation_parse_mode=ParseMode.HTML, open_period=30)

    # Set the poll message ID as the reply markup for the photo message
    await bot.send_message(chat_id=user_id, text='Please vote for your favorite picture!',
                           reply_to_message_id=poll_message.message_id)

    return poll_message.message_id


async def read_poll_results(chat_id: int, user1_id: int, user2_id: int, message_id: int):
    poll = await bot.get_poll(chat_id=chat_id, message_id=message_id)
    if poll:
        player1 = await DataBase.get_user_name(user1_id)
        player2 = await DataBase.get_user_name(user2_id)
        for option in poll.options:
            if option.text == player1:
                await DataBase.update_user_score(user1_id, option.voter_count)
            else:
                await DataBase.update_user_score(user2_id, option.voter_count)

    else:
        await bot.send_message(chat_id=chat_id, text='Poll was not found')


async def send_user_competition_result(user_id: int):
    player1 = await DataBase.get_user(user_id)
    bracket = await DataBase.get_bracket(user_id)
    for tour in bracket:
        if player1 in tour:
            player2 = tour[0] if tour[1] == player1 else tour[1]
            break
    result = compare_scores(player1.gamescore, player2.gamescore)
    if result:
        await bot.send_message(chat_id=user_id, text=f'Congratulations! You won! Your score is {player1.gamescore}')
    else:
        await bot.send_message(chat_id=user_id, text=f'You lost! Your score is {player1.gamescore}')


async def main():
    await dp.start_polling()


# Start the bot
if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling())
    except KeyboardInterrupt:
        print("Bot stopped manually")
        # asyncio.run(dp.stop_polling())
