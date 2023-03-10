""" import requirements to run game """
import os
import time
import platform
import random
import string
import getpass
from tabulate import tabulate
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hangman_highscores')

scores = SHEET.worksheet('highscore_summary')
scores_data = SHEET.worksheet('score_records')

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
            "red": "\u001b[31m",
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
winner = TextFormatting("winner")
game_over = TextFormatting("hangman0")
intro = TextFormatting("""

Lets play Hangman!

The rules are simple, the object of the game is to guess the
title of the movie.

You can guess one letter at a time, if correct you will see it appear!
If you make an incorrect guess then you lose one of your 9 lives.

Your game will be timed! If you complete your movie, see if you can make
the top 10 quickest games!

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
    choices = ("disney", "horror", "comedy", "scifi")

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
Choices are either Disney, Comedy, SciFi, or Horror...
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
    print("\n" + display + "\n")


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


def user_guesses(g_remaining, word, incorrect_g, guesses):
    """ Runs user guesses """

    start_time = time.time()

    while g_remaining > 0:
        error = ""
        input_error(word, error, g_remaining, incorrect_g, guesses)
        while True:
            try:
                guess = input("Guess a letter: ").lower().strip()
                if len(guess) != 1:
                    error = f"""
You entered '{guess}'
Please only enter one guess at a time!"""
                    input_error(word, error, g_remaining, incorrect_g, guesses)
                elif guess not in string.ascii_lowercase:
                    error = f"""
Ooops! You entered '{guess}'
Please enter a valid letter..."""
                    input_error(word, error, g_remaining, incorrect_g, guesses)
                elif guess in incorrect_g:
                    error = f"""
You have already guessed '{guess}'
Please try again!"""
                    input_error(word, error, g_remaining, incorrect_g, guesses)
                elif guess in guesses:
                    error = f"""
You have already guessed '{guess}'
Please try again!"""
                    input_error(word, error, g_remaining, incorrect_g, guesses)
                else:
                    guesses.append(guess)
                    break
            except ValueError():
                print("Please enter a letter for your next guess")

        if guess not in word:
            g_remaining = g_remaining - 1
            incorrect_g.append(guess)

            if g_remaining == 0:
                clr_scr()
                end_time = time.time()
                print(game_over.color_ascii())
                print(f"Oh no! The movie was... {word.upper()}")
                time.sleep(0.5)
                end_choice()
        else:
            word_check = word_complete(word, guesses)

            if word_check == "complete":
                clr_scr()
                print(winner.color_ascii())
                end_time = time.time()

                # slow type text
                slow_text = "You correctly guessed the movie..."
                show_movie = TextFormatting(slow_text)
                show_movie.type_delay()
                time.sleep(0.5)
                print(word.upper() + "\n")
                g_remaining = 0
                time.sleep(0.5)

                game_timer(start_time, end_time)


def input_error(word, error, g_remaining, incorrect_g, guesses):
    """ hangman game guess display """

    clr_scr()

    hangman = TextFormatting(f"hangman{g_remaining}")

    print(hangman.color_ascii())

    if len(incorrect_g) == 0:
        print("Incorrect guesses: None")
    else:
        incorrect_display = " ".join(incorrect_g)
        print(f"Incorrect guesses: {incorrect_display}")

    print_word(word, guesses)
    print(error + "\n")


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
    incorrect_g = []

    # starting lives for game
    g_remaining = 9

    user_guesses(g_remaining, word, incorrect_g, guesses)


def game_timer(start_time, end_time):
    """ Calcualted how long it took to complete game """

    secs = end_time - start_time

    if secs < 60:
        display = time.strftime("%S seconds", time.gmtime(secs))
    else:
        display = time.strftime("%M mins and %S seconds", time.gmtime(secs))

    print(f"You completed this in {display}!\n")

    score(secs)


def score(secs):
    """ Obtains user name against time score and records it to gspread """

    score_str = """
To see if you are in the top 10 quickest games, enter your name below

"""
    score_text = TextFormatting(score_str)
    score_text.type_delay()

    while True:
        try:
            user = input("Name => ").strip()
            if user == "":
                print("Please enter your name to continue.")
            else:
                break
        except ValueError():
            print("Please enter your name to continue.")

    timer = int(secs)
    data = [user, timer]

    scores_data.append_row(data)

    loading_str = "Loading highscores......\n"
    loading_text = TextFormatting(loading_str)
    loading_text.type_delay()
    time.sleep(0.5)

    high_scores = scores.get_all_values()
    print("\n HIGHSCORES")
    print(tabulate(high_scores, headers='firstrow', tablefmt="fancy_grid"))

    end_choice()


def end_choice():
    """ Provides user option to end or play again """

    prompt = '\nPlease press enter to play again!'
    getpass.getpass(prompt=prompt)

    print(title.color_ascii())
    print(selection.color_ascii())
    run_game()


def main():
    """ Run game """
    game_intro()
    run_game()


main()
