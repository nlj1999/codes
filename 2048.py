import curses
from random import randrange, choice
from collections import defaultdict

actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions_dict = dict(zip(letter_codes, actions * 2))

def get_user_action(keyboard):
	char = "N"
	while char not in actions_dict:
		char = keyboard.getch()
	return actions_dict[char]

def transpose(field):
	return [list(row) for row in zip(*field)]
def invert(field):
	return [row[::-1] for row in field]
	
class GameField(object):
	def __init__(self, height = 4, width = 4):
		self.height = height
		self.width = width
		self.score = 0
		self.highscore = 0
		self.reset()
	
	def spawn(self):
		new_element = 4 if randrange(100) > 89 else 2
		(i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if not self.field[i][j]])
		self.field[i][j] = new_element
		
	def reset(self):
		self.score = 0
		self.field = [[0 for i in range(self.width)] for j in range(self.height)]
		self.spawn()
		self.spawn()
	
	def move_possible(self,direction):
		def row_possible(row):
			def examine(i):
				return (row[i] == 0 and row[i+1] != 0) or (row[i] != 0 and row[i] == row[i+1])
			return any(examine(i) for i in range(len(row)-1))
		
		check = {}
		check['Left'] = lambda field: any(row_possible(row) for row in field)
		check['Right'] = lambda field: check['Left'](invert(field))
		check['Up'] = lambda field: check['Left'](transpose(field))
		check['Down'] = lambda field: check['Right'](transpose(field))
		
		if direction in check:
			return check[direction](self.field)
		return False
		
	def move(self, direction):
		def move_left(row):
			def squeeze(row):
				new_row = [i for i in row if i]
				new_row += [0 for i in range(len(row)-len(new_row))]
				return new_row
			
			def merge(row):
				pair = False
				new_row = []
				for i in range(len(row)):
					if pair:
						new_row.append(2*row[i])
						self.score += 2*row[i]
						self.highscore = max(self.highscore,self.score)
						pair = False
					elif i+1 < len(row) and row[i] == row[i+1]:
						pair = True
						new_row.append(0)
					else:
						new_row.append(row[i])
				assert len(new_row) == len(row)
				return new_row
			return squeeze(merge(squeeze(row)))
		
		moves = {}
		moves['Left'] = lambda field: [move_left(row) for row in field]
		moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
		moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
		moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))
		
		if direction in moves:
			if self.move_possible(direction):
				self.field = moves[direction](self.field)
				self.spawn()
				return True
			return False
		
	def is_gameover(self):
		return not any(self.move_possible(move) for move in actions)
	
	def draw(self, screen):
		help_string1 = '(W)Up (S)Down (A)Left (D)Right'
		help_string2 = '      (R)Restart (Q)quit'
		gameover_string = '        Game Over'
		
		def cast(string):
			screen.addstr(string+'\n')
		def separator():
			cast('+------'*self.width + '+')
		def draw_row(row):
			cast(''.join('|{: ^6}'.format(num) if num > 0 else '|      ' for num in row) + '|')
		screen.clear()
		cast('SCORE: ' + str(self.score))
		cast('HIGHSCORE: ' + str(self.highscore))
		for row in self.field:
			separator()
			draw_row(row)
		separator()
		if self.is_gameover():
			cast(gameover_string)
		else:
			cast(help_string1)
		cast(help_string2)

def main(stdscr):
	def init():
		game_field.reset()
		return 'Game'
	
	def not_game(state):
		game_field.draw(stdscr)
		action = get_user_action(stdscr)
		responses = defaultdict(lambda: state)
		responses['Restart'], response['Exit'] = 'Init', 'Exit'
		return responses[action]
	
	def game():
		game_field.draw(stdscr)
		action = get_user_action(stdscr)
		if action == 'Restart':
			return 'Init'
		if action == 'Exit':
			return 'Exit'
		if game_field.move(action):
			if game_field.is_gameover():
				return 'Gameover'
		return 'Game'
	state_actions = {
		'Init':init,
		'Gameover': lambda: not_game('Gameover'),
		'Game': game
	}
	curses.use_default_colors()
	game_field = GameField()
	
	state = 'Init'
	while state != 'Exit':
		state = state_actions[state]()

curses.wrapper(main)
