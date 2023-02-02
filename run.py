"""imports system for ascii escape codes readability"""
import os
import time

os.system("")


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
            time.sleep(0.06)


# Instances of text formatting class
title = TextFormatting("title")
selection = TextFormatting("movie_selection")
intro = TextFormatting("""

Lets play Hangman!

The rules are simple, the object of the game is to guess the
title of the movie.

You can guess one letter at a time and if correct you will see it appear!
If you make an incorrect guess then you loose one of your 9 lives.

Please see below movie genres to choose from...

""")


# Game introduction
print(title.color_ascii())


# type_delay(INTRO)
intro.type_delay()

time.sleep(0.5)
print(selection.color_ascii())


def select_mode():
    """ User selects mode to play from """

    input_prompt = "Please enter the genre of movie you would like to play: "
    choices = ("disney", "horror", "comedy", "sci-fi")

    while True:

        try:
            user_choice = input(input_prompt).strip().lower()
        except ValueError:
            print("Please try again... ")
            continue

        if user_choice not in choices:
            print("""
Ooops! That doesn't match an option!

Please try either disney, comedy, sci-fi, or horror...
""")
        else:
            return user_choice


select_mode()
