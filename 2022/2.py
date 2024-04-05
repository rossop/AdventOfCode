with open('in/2.input') as file:
  lines = file.read().strip().split('\n')


### Part 1
def count_score(outcome: str, hand: str) -> int:
  hand_score = {'rock': 1, 'paper': 2, 'scissors': 3}
  outcome_score = {'win': 6, 'draw': 3, 'loose': 0}

  return hand_score[hand] + outcome_score[outcome]


def determine_winner(other_player: str, you_player: str) -> str:
  rules = {'paper': 'rock', 'scissors': 'paper', 'rock': 'scissors'}

  if you_player == other_player:
    return 'draw'
  elif rules[you_player] == other_player:
    return 'win'
  else:
    return 'loose'


encryption = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
strategy = {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}

plays = [(encryption[line.split()[0]], strategy[line.split()[1]])
         for line in lines]

score = 0
for play in plays:
  score += count_score(determine_winner(*play), play[1])

print('Part 1:  ' + str(score))

### Part 2

encryption = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
strategy = {'X': 'loose', 'Y': 'draw', 'Z': 'win'}


def determine_hand(hand: str, strategy: str) -> str:
  loose_rules = {'paper': 'rock', 'scissors': 'paper', 'rock': 'scissors'}
  win_rules = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}

  if strategy == 'win':
    return win_rules[hand]
  elif strategy == 'draw':
    return hand
  else:
    return loose_rules[hand]


plays = [(encryption[line.split()[0]], strategy[line.split()[1]])
         for line in lines]

score = 0
for play in plays:
  score += count_score(play[1], determine_hand(*play))

print('Part 2:  ' + str(score))