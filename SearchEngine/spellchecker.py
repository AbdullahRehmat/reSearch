"""
    Basic Spell Checker & Punctuation Stripper
    Used To Standarise Spelling According To 
    Provided JSON Dictionary.
"""

import os
import json
import unicodedata


class SpellChecker:
    def __init__(self) -> None:
        self.wl_file = "wordlist.json"
        self.wordlist = {}

    def _load_wordlist(self) -> None:
        """ Loads JSON Wordlist From Local Directory """

        path = os.path.join(os.path.dirname(__file__), self.wl_file)
        file = open(path)
        data = json.load(file)
        self.wordlist = data["dictionary"]

    def strip_punctuation(self, text: str) -> str:
        """ Removes Excess Punctuation """

        punctuation = "!#$%'*+,./;<=>?@[\]^_`{|}~()"
        new_text = text.translate(str.maketrans("", "", punctuation))

        return new_text

    def strip_accents(self, text: str) -> str:
        """ Removes Accent Marks From Letters """

        nfkd_form = unicodedata.normalize("NFKD", text)
        ascii_form = nfkd_form.encode("ASCII", "ignore")
        new_text = str(ascii_form.decode("utf-8"))

        return new_text

    def format_spaces(self, text: str) -> str:
        """ Removes Double, Leading & Trailing Spaces """

        # Remove Double Spaces
        if "  " in text:
            text = text.replace("  ", " ")

        else:
            pass

        # Remove Leading & Trailing Spaces
        new_text = text.strip()

        return new_text

    def fix_spelling(self, text: str) -> str:
        """ Correct Spelling In Accordance To Provided Wordlist """

        # Loads JSON Wordlist File Into Memory
        self._load_wordlist()

        # k = correctly spelled word
        # v = list of incorrectly spelled versions of "k"
        # i = iterate through list "v"

        for k, v in self.wordlist.items():
            for i in v:
                if i.lower() in text:
                    new_text = text.replace(i.lower(), k.title())
                    return new_text

                elif i.title() in text:
                    new_text = text.replace(i.title(), k.title())
                    return new_text

        else:
            return text

    def run_spell_checker(self, text: str) -> str:
        """ Runs All Functions On Provided Text """

        if type(text) != str:
            return str(text)

        text = self.strip_punctuation(text)
        text = self.strip_accents(text)
        text = self.format_spaces(text)
        text = self.fix_spelling(text)

        return text


if __name__ == "__main__":

    print("Library Running In TEST MODE...")
    input_text = input("Enter Text: ")

    s = SpellChecker()
    corrected_text = s.run_spell_checker(input_text)
    print("Corrected Text: " + corrected_text)
