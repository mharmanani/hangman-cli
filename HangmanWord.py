import HangingMan

class deadPlayerException(Exception):
	pass

class HangmanWord:
	"""
	A class to model words in the game hangman
	"""
	def __init__(self, word):
		self.visible, self.blurred, self.tries = [], [], []
		self.wrong_guesses = 0
		self._hanging_man = HangingMan.hangings[self.wrong_guesses]
		for chr in word:
			self.visible.append(chr)
			self.blurred.append('_')
		self.blurred[0], self.blurred[-1] = self.visible[0], self.visible[-1]

	def __repr__(self):
		blurred_word = ''
		for char in self.blurred:
			blurred_word += char
		return blurred_word

	def take_a_guess(self, letter):
		assert letter != 'quit'
		print("You have tried: ", self.tries)
		if letter in self.visible and letter not in self.tries:
			for i in range(len(self.visible)):
				if self.visible[i] == letter:
					self.blurred[i] = letter
			print(self)
			self.tries.append(letter)
		elif letter in self.tries:
			print("You already tried this letter...")
		elif letter not in self.visible:
			print("There is no ", letter, " in ", str(self))
			self.wrong_guesses += 1
			self.tries.append(letter)
		print(HangingMan.hangings[self.wrong_guesses])
		if self.wrong_guesses >= 8:
			raise deadPlayerException

	def generate_hanging_man(self):
		return self._hanging_man