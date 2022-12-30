import os
import json
import unicodedata


class SpellChecker:
    def __init__(self) -> None:
        self.wl_addr = "wordlist.json"
        self.wordlist = {}

    def _load_wordlist(self) -> None:
        path = os.path.join(os.path.dirname(__file__), self.wl_addr)
        file = open(path)
        data = json.load(file)
        self.wordlist = data["dictionary"]

    def strip_punctuation(self, text: str) -> str:
        punctuation = "!#$%'*+,./;<=>?@[\]^_`{|}~()"
        new_text = text.translate(str.maketrans("", "", punctuation))

        return new_text

    def strip_accents(self, text: str) -> str:
        nfkd_form = unicodedata.normalize("NFKD", text)
        ascii_form = nfkd_form.encode("ASCII", "ignore")
        new_text = str(ascii_form.decode("utf-8"))

        return new_text

    def format_spaces(self, text: str) -> str:
        if "  " in text:
            new_text = text.replace("  ", " ")
            return new_text

        else:
            return text

    def fix_spelling(self, text: str) -> str:
        self._load_wordlist()

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

    def spell_checker(self, text: str) -> str:

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
    corrected_text = s.spell_checker(input_text)
    print("Corrected Text: " + corrected_text)
