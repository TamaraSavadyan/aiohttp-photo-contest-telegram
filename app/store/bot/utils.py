import random

def generate_tournament_bracket(players):
    random.shuffle(players)
    bracket = []
    for i in range(0, len(players), 2):
        if i + 1 == len(players):
            bracket.append((players[i], None))
        else:
            bracket.append((players[i], players[i + 1]))
    
    text = ''
    for br in bracket:
        text += f'{br[0]}\tvs\t{br[1]}\n\n'

    return text, bracket

def compare_scores(score1, score2):
    if score1 > score2:
        return 1
    elif score1 < score2:
        return 0
    else:
        chosen = random.choice(score1, score2)
        if chosen == score1:
            score1 += 0.005
        else:
            score2 += 0.005

        return compare_scores(score1, score2)
