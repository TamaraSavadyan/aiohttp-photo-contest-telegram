import pytest

from app.utils import generate_tournament_bracket, compare_scores

@pytest.fixture
def players():
    return ['Player1', 'Player2', 'Player3', 'Player4']

def test_generate_tournament_bracket(players):
    text, bracket = generate_tournament_bracket(players)
    assert len(bracket) == 2
    assert len(text.strip().split('\n')) == 2
    assert (players[0], players[1]) in bracket or (players[1], players[0]) in bracket
    assert (players[2], players[3]) in bracket or (players[3], players[2]) in bracket

def test_compare_scores():
    score1 = 1.0
    score2 = 1.0
    assert compare_scores(score1, score2) == 1 or compare_scores(score1, score2) == 0