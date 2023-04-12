from unittest.mock import AsyncMock, Mock, patch
from aiogram.types import Message, Poll, PollType, ParseMode
import pytest
from app.database import User, DataBase

from app.manager import bot, dp, create_poll, send_ticking_clock, read_poll_results, send_user_competition_result, start_command_handler, stop_command_handler, get_profile_picture, send_picture_to_user, send_tournament_bracket


@pytest.fixture
async def sent_message():
    message = await bot.send_message(chat_id=123, text='test')
    yield message
    await bot.delete_message(chat_id=123, message_id=message.message_id)


async def test_send_ticking_clock(sent_message):
    await send_ticking_clock(user_id=123, duration=5)
    edited_message = await bot.get_message(chat_id=123, message_id=sent_message.message_id)
    assert edited_message.text == '00:05'


@pytest.mark.asyncio
async def test_get_profile_picture():
    # Create a mock Message object with the required from_user.id attribute
    message = Message(message_id=1, from_user=Mock(
        id=123), date=None, chat=None, text=None)

    # Call the function and check the returned file_id matches the mocked value
    result = await get_profile_picture(message)
    assert result == '1234'


async def test_send_picture_to_user(setup_user, mocker):
    # create a mock of the bot's send_photo method
    mocker.patch.object(bot, 'send_photo')

    # create a mock message object with the test user's id
    message = Message(message_id=1, from_user=setup_user)

    # call the function with the mock message
    await send_picture_to_user(message)

    # check that the send_photo method was called with the correct arguments
    bot.send_photo.assert_called_once_with(
        chat_id=setup_user.id_, photo=setup_user.avatar_link)


@pytest.mark.asyncio
async def test_send_tournament_bracket():
    # Create a mock user ID
    user_id = 123456

    # Create a mock player list
    mock_players = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
    mock_database = Mock()
    mock_database.get_users_names.return_value = mock_players

    # Create a mock bracket
    mock_bracket = [('Player 1', 'Player 2'), ('Player 3', 'Player 4')]
    mock_generate_bracket = Mock(return_value=(
        'Player 1 vs Player 2\n\nPlayer 3 vs Player 4\n\n', mock_bracket))

    # Create a mock bot instance
    mock_bot = Mock()

    # Call the function
    await send_tournament_bracket(user_id, mock_database, mock_generate_bracket, mock_bot)

    # Assert that the bracket was saved to the database
    mock_database.save_bracket.assert_called_once_with(user_id, mock_bracket)

    # Assert that the bracket was sent to the user
    mock_bot.send_message.assert_called_once_with(
        chat_id=user_id, text='Here is current tournament bracket:\n\nPlayer 1 vs Player 2\n\nPlayer 3 vs Player 4\n\n')


@pytest.mark.asyncio
async def test_create_poll():
    # set up test data
    user_id = 123
    player1 = User(id_=1, first_name='John', last_name='Doe',
                   score=5.0, avatar_link='photo1.jpg')
    player2 = User(id_=2, first_name='Jane', last_name='Doe',
                   score=4.5, avatar_link='photo2.jpg')
    bracket = [(player1, player2)]

    # mock the necessary functions from the bot API
    bot.upload_photo = AsyncMock(return_value='photo_url')
    bot.send_poll = AsyncMock(return_value=Poll(id_='123', question='Which picture do you like better?', options=[
                              'John Doe', 'Jane Doe'], type=PollType.REGULAR, allows_multiple_answers=False))
    bot.send_message = AsyncMock(return_value=None)

    # run the function
    poll_message_id = await create_poll(user_id, bot, bracket)

    # assert that the necessary bot API functions were called
    bot.upload_photo.assert_called_with(open('photo1.jpg', 'rb'))
    bot.upload_photo.assert_called_with(open('photo2.jpg', 'rb'))
    bot.send_poll.assert_called_with(chat_id=user_id, question='Which picture do you like better?', options=[
                                     'John Doe', 'Jane Doe'], type=PollType.REGULAR, allows_multiple_answers=False, is_anonymous=True, explanation="Please vote for your favorite picture!", explanation_parse_mode=ParseMode.HTML, open_period=30)
    bot.send_message.assert_called_with(
        chat_id=user_id, text='Please vote for your favorite picture!', reply_to_message_id=poll_message_id)


async def test_read_poll_results_success():
    # Arrange
    chat_id = 123456
    user1_id = 123
    user2_id = 456
    await dp.skip_updates()
    await DataBase.add_user(user1_id, 'Player 1', 'photo1.jpg')
    await DataBase.add_user(user2_id, 'Player 2', 'photo2.jpg')
    poll = Poll(
        question='Which picture do you like better?',
        options=[f"Player 1", f"Player 2"],
        type=PollType.REGULAR,
        allows_multiple_answers=False,
    )
    poll_message = await bot.send_poll(
        chat_id=chat_id,
        question=poll.question,
        options=poll.options,
        type=poll.type,
        allows_multiple_answers=poll.allows_multiple_answers,
        is_anonymous=True,
        explanation="Please vote for your favorite picture!",
        explanation_parse_mode=ParseMode.HTML,
        open_period=30,
    )
    await bot.stop_poll(chat_id=chat_id, message_id=poll_message.message_id)

    # Act
    await read_poll_results(chat_id, user1_id, user2_id, poll_message.message_id)

    # Assert
    assert await DataBase.get_user_score(user1_id) == 1
    assert await DataBase.get_user_score(user2_id) == 0


@pytest.mark.asyncio
async def test_send_user_competition_result():
    # create a test user
    user_id = 12345
    player1 = User(id=user_id, first_name='John', last_name='Doe', gamescore=5)

    # create a test bracket
    bracket = [[player1, User(id=6789, first_name='Jane', last_name='Doe', gamescore=3)]]

    # mock the get_user and get_bracket functions from the database
    mock_get_user = AsyncMock(return_value=player1)
    mock_get_bracket = AsyncMock(return_value=bracket)

    # patch the get_user and get_bracket functions to use the mocks
    with patch('app.database.get_user', mock_get_user), \
         patch('app.database.get_bracket', mock_get_bracket), \
         patch('app.bot.send_message') as mock_send_message:

        # call the function being tested
        await send_user_competition_result(user_id)

        # assert that the appropriate message is sent to the user
        mock_send_message.assert_called_once_with(chat_id=user_id, text=f'Congratulations! You won! Your score is {player1.gamescore}')


