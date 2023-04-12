import pytest
from app.database import User, DataBase

@pytest.fixture
def users():
    return [
        User(id_=1, first_name="John", last_name="Doe", avatar_link="https://example.com/avatar1.png", score=4.5),
        User(id_=2, first_name="Jane", last_name="Smith", avatar_link="https://example.com/avatar2.png", score=3.2),
        User(id_=3, first_name="Bob", last_name="Johnson", avatar_link="https://example.com/avatar3.png", score=2.8),
    ]

@pytest.fixture
def user():
    user_id = 123
    first_name = "John"
    last_name = "Doe"
    score = 4.5
    avatar_link = "http://example.com/avatar.jpg"
    return User(user_id, first_name, last_name, score, avatar_link)

async def test_add_user(users, user):
    await DataBase.add_user(user.id, user.first_name, user.last_name, user.score, user.avatar_link)
    
    assert len(users) == 1
    assert isinstance(users[0], User)
    assert users[0].id == user.id
    assert users[0].first_name == user.first_name
    assert users[0].last_name == user.last_name
    assert users[0].score == user.score
    assert users[0].avatar_link == user.avatar_link


async def test_get_user(users):
    # Arrange
    user1 = User(1, "John", "Doe", "https://example.com/avatar1.jpg", 0)
    user2 = User(2, "Jane", "Doe", "https://example.com/avatar2.jpg", 0)
    users.append(user1)
    users.append(user2)

    # Act
    result = await DataBase.get_user(1)

    # Assert
    assert result == user1


async def test_delete_user(users):
    # Delete user with id=2
    await DataBase.delete_user(id_=2)

    for user in users:
        assert user.id_ != 2

    await DataBase.delete_user(id_=1)

    for user in users:
        assert user.id_ != 1
    await DataBase.delete_user(id_=3)
    assert len(users) == 2

async def test_update_user(users):
    # Update user with id=2
    await DataBase.update_user(id_=2, first_name="Jane", last_name="Smith", score=3.2, avatar_link="https://example.com/avatar2.png")

    # Check that user with id=2 is updated
    for user in users:
        if user.id_ == 2:
            assert user.first_name == "Jane"
            assert user.last_name == "Smith"
            assert user.score == 3.2
            assert user.avatar_link == "https://example.com/avatar2.png"

    # Try to update user with id=4 (which does not exist)
    await DataBase.update_user(id_=4, first_name="Jane", last_name="Smith", score=3.2, avatar_link="https://example.com/avatar2.png")

    # Check that the list of users is still the same
    assert len(users) == 2

async def test_get_users(users):
    # Arrange
    user1 = User(1, "John", "Doe", "https://example.com/avatar1.jpg", 0)
    user2 = User(2, "Jane", "Doe", "https://example.com/avatar2.jpg", 0)
    users.append(user1)
    users.append(user2)

    # Act
    result = await DataBase.get_users()

    # Assert
    assert result == users


async def test_get_users_names(users):
    # Arrange
    user1 = User(1, "John", "Doe", "https://example.com/avatar1.jpg", 0)
    user2 = User(2, "Jane", "Doe", "https://example.com/avatar2.jpg", 0)
    users.append(user1)
    users.append(user2)

    # Act
    result = await DataBase.get_users_names()

    # Assert
    assert result == ["John Doe", "Jane Doe"]

async def test_update_user_score(users):
    # Update user with id=2
    await DataBase.update_user_score(id_=2, score=3.2)

    # Check that user with id=2 is updated
    for user in users:
        if user.id_ == 2:
            assert user.score == 3.2

    # Try to update user with id=4 (which does not exist)
    await DataBase.update_user_score(id_=4, score=3.2)

    # Check that the list of users is still the same
    assert len(users) == 2

async def test_reset_score(users):
    # Reset user with id=2
    await DataBase.reset_score(id_=2)

    # Check that user with id=2 is updated
    for user in users:
        if user.id_ == 2:
            assert user.score == 0

    # Try to reset user with id=4 (which does not exist)
    await DataBase.reset_score(id_=4)

    # Check that the list of users is still the same
    assert len(users) == 2

async def test_get_user_name(users):
    # Arrange
    user1 = User(1, "John", "Doe", "https://example.com/avatar1.jpg", 0)
    user2 = User(2, "Jane", "Doe", "https://example.com/avatar2.jpg", 0)
    users.append(user1)
    users.append(user2)

    # Act
    result = await DataBase.get_user_name(1)

    # Assert
    assert result == "John Doe"

async def test_clear_users(users):
    # Clear users
    await DataBase.clear_users()

    # Check that the list of users is empty
    assert len(users) == 0


