"""imports system for ascii escape codes readability"""
import os
import time
import platform
import random


os.system("")


def clr_scr():
    """ function  to clear screen """

    if platform.system().lower() == "windows":
        cmd = 'cls'
    else:
        cmd = 'clear'

    os.system(cmd)


class TextFormatting:
    """ take in name of ascii file for formatting"""

    def __init__(self, text):
        self.text = text

    def color_ascii(self):
        """ replaces color with ascii escape codes"""

        font_colors = {
            "green": "\u001b[32m",
            "yellow": "\u001b[33;1m",
            "blue": "\u001b[34;1m",
            "white": "\u001b[37m",
            "red":  "\u001b[31m",
            "cyan": "\u001b[36m"
            }

        file = f"./assets/ascii_docs/{self.text}.txt"
        content = open(file, "r", encoding="utf-8")
        data = "".join(content.readlines())

        for color, code in font_colors.items():
            data = data.replace("[[" + color + "]]", code)

        return data

    def type_delay(self):
        """ Adds seconds between letter print in console """
        for letter in self.text:
            print(letter, end="", flush=True)
            time.sleep(0.04)


# Instances of text formatting class
title = TextFormatting("title")
selection = TextFormatting("movie_selection")
intro = TextFormatting("""

Lets play Hangman!

The rules are simple, the object of the game is to guess the
title of the movie.

You can guess one letter at a time and if correct you will see it appear!
If you make an incorrect guess then you lose one of your 9 lives.

Please see below movie genres to choose from...

""")


def game_intro():
    """ main intro to game """

    print(title.color_ascii())
    intro.type_delay()
    time.sleep(0.5)

    # print movie genre ascii
    print(selection.color_ascii())


def select_mode():
    """ User selects mode to play from """

    prompt_str = "Please enter the genre of movie you would like to play"
    input_prompt = TextFormatting(prompt_str)
    choices = ("disney", "horror", "comedy", "sci-fi")

    while True:

        try:
            input_prompt.type_delay()
            user_choice = input("  =>  ").strip().lower()
        except ValueError:
            print("Please try again... ")
            continue

        if user_choice not in choices:
            print("""
Ooops! That doesn't match an option!
Choices are either Disney, Comedy, Sci-Fi, or Horror...
""")
        else:
            print("\nGreat Choice! Let's Go!")
            time.sleep(2)
            clr_scr()
            return user_choice


def print_word(word, guesses):
    """creates hang man display after guess for player"""
    result = []
    for letter in word:
        if letter in guesses:
            result.append(letter + " ")
        else:
            result.append("_ ")

    display = "".join(result)
    print("\n"+display+"\n")


def word_complete(word, guesses):
    """ create comparable string to word """

    compare = []

    for letter in word:
        if letter in guesses:
            compare.append(letter)
        else:
            compare.append("_")

    # compare result to word to see if correct/finished
    result_compare = "".join(compare)

    if result_compare == word:
        return "complete"

    return "incomplete"


def run_game():
    """ Runs though game """

    user_choice = select_mode()
    # selects correct file for user choice
    word_file = f"./assets/word_selections/{user_choice}_movies.txt"
    movie_mode = open(word_file, "r", encoding="utf-8")
    word_list = movie_mode.readlines()

    # select random word for game play
    word = random.choice(word_list).lower()[:-1]

    # create empty list to hold guesses, includes space
    guesses = [" "]

    # starting lives for game
    guesses_remaining = 9
    print(word)

    print_word(word, guesses)

    while guesses_remaining > 0:
        guess = input("Guess a letter: ").lower()

        guesses.append(guess)

        if guess not in word:
            guesses_remaining = guesses_remaining - 1

            if guesses_remaining == 0:
                continue

        print_word(word, guesses)
        print(f"Lives left {guesses_remaining}\n")

    print("Game Over!")


game_intro()
run_game()
