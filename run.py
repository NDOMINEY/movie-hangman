"""imports system for ascii escape codes readability"""
import os

os.system("")


class AnsciiFormatting:
    """ take in name of ascii file for formatting"""

    def __init__(self, text):
        self.text = text

    def color_anscii(self):
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
        anscii = "".join(content.readlines())

        for color, code in font_colors.items():
            anscii = anscii.replace("[[" + color + "]]", code)

        return anscii


title = AnsciiFormatting("title")


print(title.color_anscii())
