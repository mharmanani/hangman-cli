"""
hangman.py
Mohamed Harmanani, 2017
"""
import random
from HangmanWord import *
from HangingMan import *
import getpass

ROOT = '.lang/'
#modules for pick_language
LANGUAGES = { 0: 'english', 
			  1: 'french', 
			  2: 'spanish' }
MAX_LANG_INDEX = max(list(LANGUAGES.keys()))
MIN_LANG_INDEX = min(list(LANGUAGES.keys()))

#modules for pick_length
class InvalidLengthException(Exception):
	pass

class InvalidNumberOfPlayersException(Exception):
	pass

def pick_number_of_players():
	"""
	Prompts the user to choose how many players will play.
	@rtype: int
	"""
	chosen = False
	while not chosen:
		try:
			num = int(input("How many players would you like? (1/2) "))
		except:
			print("Please enter an integer.")
		if num < 1 or num > 2:
			print("Please pick 1 or 2 players.")
			continue
		chosen = True
	return num

def pick_language():
	"""
	Prompts the user to choose the language he desires to play in.
	@rtype: str
	"""
	NO_LANGUAGE_SELECTED = True
	print("Welcome to Hangman")
	print("Please select any of the following languages")
	while NO_LANGUAGE_SELECTED:
		lang_index = input("English (0)" 
			              + '\n' + "Français(1)" 
			              + '\n' + "Español (2)" 
			              + '\n' + "Enter the number of your desired language: ")
		try:
			lang_index = int(lang_index)
			assert lang_index >= MIN_LANG_INDEX and lang_index <= MAX_LANG_INDEX
		except:
			print("An error has occurred, try again...")
			continue
		NO_LANGUAGE_SELECTED = False
	lang = LANGUAGES[lang_index]
	return lang

def get_word_list(fname):
	"""
	Uses the data from pick_language to generate a list of words in the
	language selected by the user.
	@param str fname: name of the file to read from
	@rtype: list[str]
	"""
	fhand = open(fname)
	words = fhand.readlines()
	words = [word.strip() for word in words]
	return words

def pick_length(word_lst, word_len):
	"""
	Initializes a randomly generated word of length word_len from word_lst.
	@param list[str] word_lst: list of words
	@param int word_len: length of the word to be selected
	@rtype: 
	"""
	def has_desired_size(word):
		""" (str, int) -> bool
		"""
		return len(word) == word_len
	if word_len <= 2:
		raise InvalidLengthException
	sized_lst = list(filter(has_desired_size, word_lst))
	return sized_lst

def main():
	print("--------------- Welcome to Hangman")
	guessed = False
	number_of_players = pick_number_of_players()
	if number_of_players == 1:
		lang = ROOT + pick_language() + '.txt'
		word_lst = get_word_list(lang)
		try:
			word_len = int(input("Pick the length of your desired word (>2) : "))
			sized_lst = pick_length(word_lst, word_len)
		except ValueError:
			print("You have not entered a valid number, we have selected the length at random.")
			word_len = random.randint(1,10)
		except InvalidLengthException:
			print("Your word is too short, we have selected the length at random.")
			word_len = random.randint(1,10)
		sized_lst = pick_length(word_lst, word_len)
		chosen_word = HangmanWord(random.choice(sized_lst))
	elif number_of_players == 2:
		print("Have one player choose the word, and the other guess:")
		chosen_word = HangmanWord(getpass.getpass("Your word here: "))
	print("Your word is " + str(chosen_word))
	while not guessed:
		letter = input("Take a guess (quit to end game): ")
		try:
		    chosen_word.take_a_guess(letter)
		except AssertionError:
			print("You have chosen to quit the game...")
			break
		except deadPlayerException:
			print("You have failed to complete the word", 
				  ''.join(chosen_word.visible))
			print("You are dead...")
			break
		if chosen_word.visible == chosen_word.blurred:
			print("You have successfully completed the word", str(chosen_word))
			guessed = True

if __name__ == '__main__':
	main()
