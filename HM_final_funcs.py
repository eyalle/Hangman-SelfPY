import random
import colorsys
import os
from colored import fg, bg, attr



def get_secret_word():
    return SECRET_WORD

def pri(str):
    TEXT_COLOR = fg(199)
    RES = attr('reset')

    print (TEXT_COLOR, str, RES)

def start_game(WORDS_FILE_PATH, WORD_INDEX):
    """
    start_game will be responsible for tha management of the game.
    It will basically interact with the user and call functions.

    :param WORDS_FILE_PATH: string representing a file with words in it
    :param WORD_INDEX: string an index to use for choosing the word to be guessed
    :type WORDS_FILE_PATH: string
    :type WORD_INDEX: string

    :return:
    :rtype:
    """

    letters_guessed = ["!"]
    os.system('clear')
    pri_logo()

    global SECRET_WORD
    SECRET_WORD = choose_word(WORDS_FILE_PATH, int(WORD_INDEX))[1]
    ALLOWED_TRYS = len(SECRET_WORD)

    while (not(check_win(letters_guessed)) and ALLOWED_TRYS > 0):
        char_guessed = input("Please guess a letter\n")
        while (not(check_valid_input(char_guessed, letters_guessed))):
            pri("please use valid english characters only, and not letters already guessed.\n")
            char_guessed = input()
        ALLOWED_TRYS = print_hangman(ALLOWED_TRYS, char_guessed)
        print (show_hidden_word(letters_guessed))

    if (ALLOWED_TRYS > 0):
        pri ("YOU WIN ! ! !")
    else:
        pri ("you lose :(")


def is_valid_input(letter_guessed):
    """
    letter_guessed checks if the argument passed is a valid English letter or not.

    :param letter_guessed: player's char
    :type letter_guessed: str
    :return: True or False, if the player's char is in English
    :rtype: boolean
    """
    if (len(letter_guessed) > 1 or not(letter_guessed.isalpha())):
        return False

    return True

def check_valid_input(letter_guessed, old_letters_guessed):
        """
        check_valid_input checks the letter_guessed against old_letters_guessed in the following manner:
        if letter_guessed is not in old_letters_guessed, and returns True from is_valid_input(letter_guessed)
        then return True, else return False.

        :param letter_guessed: player's char
        :param old_letters_guessed: list of letters guessed
        :type letter_guessed: str
        :type old_letters_guessed: list
        :return: True or False, if the player's char is in English and not already guessed
        :rtype: boolean
        """

        if (is_valid_input(letter_guessed) and (old_letters_guessed.count(letter_guessed)) < 1):
            old_letters_guessed.append(letter_guessed)
            return True

        return False

def show_hidden_word(old_letters_guessed):
    """
    show_hidden_word recieves the secret word and the list of old letters letter_guessed
    and returns a string with the right old letters guessed and _ instead of not guessed letters

    :param old_letters_guessed: list of letters guessed
    :type old_letters_guessed: list
    :return: generated string, see above
    :rtype: str
    """

    pri (old_letters_guessed)
    successfully_guessed = ("_ " * len(SECRET_WORD)).split()
    pri (successfully_guessed)
    for char in old_letters_guessed:
        if (check_win(char)):
            successfully_guessed[get_guessed_index(char)] = char
        else:
            pri (successfully_guessed)

    pri (successfully_guessed)
    return "".join(successfully_guessed)

def check_win(old_letters_guessed):
    """
    check_win recieves the secret word and the list of old letters letter_guessed
    and True if the secret word was guessed or False, otherwise

    :param old_letters_guessed: list of letters guessed
    :type old_letters_guessed: list
    :return: True if SECRET_WORD was guessed
    :rtype: boolean
    """
    win = all([char in get_secret_word() for char in old_letters_guessed])
    return win

def check_guess (char):
    """
    check_guess a char and the secret word to guess.
            check_guess will return True if the char is in the SECRET_WORD, or False otherwise.
    :param char: a guessed character
    :type char: string

    :return: True if char is in SECRET_WORD
    :rtype: boolean
    """
    # guess = False
    # for ch in get_secret_word():
    #     if (char == ch):
    #         guess = True
    #         break
    # if (char in get_secret_word()):
    return (char in get_secret_word())

def print_hangman(num_of_tries, char):
    """
    print_hangman recieves the number of tries a user has and does the following:
        if the character guessed is valild, and is part of the secret word - print the current state of HangMan, return the same amount of guesses left.
        Else, print the HangMan pose after the unsuccessful guess, and return the num_of_tries - 1
    :param num_of_tries: player's number of tries
    :param SECRET_WORD: player's word to guess
    :type num_of_tries: int
    :type SECRET_WORD: string

    :return: the number of guesses the player has left
    :rtype: int
    """

    HANGMAN_PHOTOS =   {
    0: """
        x-------x""",
    1: """
        x-------x
        |
        |
        |
        |
        |""",
    2: """
        x-------x
        |       |
        |       0
        |
        |
        |
    """,
    3: """
        x-------x
        |       |
        |       0
        |       |
        |
        |
    """,
    4: """
        x-------x
        |       |
        |       0
        |      /|\\
        |
        |
    """,
    5: """
        x-------x
        |       |
        |       0
        |      /|\\
        |      /
        |
    """,
    6:"""
        x-------x
        |       |
        |       0
        |      /|\\
        |      / \\
        |
    """
    }

    if (is_valid_input(char) and check_guess(char)):
        pri (HANGMAN_PHOTOS[len(HANGMAN_PHOTOS)-num_of_tries-1])
        return num_of_tries
    else:
        pri (HANGMAN_PHOTOS[len(HANGMAN_PHOTOS)-(num_of_tries)])
        return num_of_tries - 1

def get_guessed_index(successfully_guessed):
    return SECRET_WORD.find(successfully_guessed)

def choose_word(file_path, index):
    """
    choose_word recieves a string-based file path, and an index.
    choose_word will return a tuple that contains - (num of unique words in file, a random word based on the index)

    :param file_path: a string representing a file
    :param index: a number
    :type file_path: string
    :type index: int

    :return: tuple of 2 elements (num of unique words in file, a random word to guess)
    :rtype: tuple
    """

    f = open(file_path, 'r')
    words = f.read().rsplit()
    f.close()
    words_set = sorted(set(words), key=words.index)
    words_limit = len(words_set)
    if (index > len(words)):
        index = index - (len(words) * (index // len(words)))

    words_list = list(words_set)

    pri ("")

    return (words_limit, words[index-1])

def pri_logo():
    HANGMAN_ASCII_ART ="""
 =============================================================
|      _    _                                                 |
|     | |  | |                                                |
|     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __          |
|     |  __  |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\         |
|     | |  | | (_| | | | | (_| | | | | | | (_| | | | |        |
|     |_|  |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|        |
|                          __/ |                              |
|                         |___/                               |
 =============================================================
    """

    pri (HANGMAN_ASCII_ART)
