import unicodedata
from wordlist import dictionary


class SpellChecker():
    def __init__(self) -> None:
        pass

    def strip_punctuation(self, text: str) -> str:
        punctuation = "!#$%'*+,./;<=>?@[\]^_`{|}~"
        new_text = text.translate(str.maketrans("", "", punctuation))

        return new_text

    def strip_accents(self, text: str) -> str:
        nfkd_form = unicodedata.normalize("NFKD", text)
        ascii_form = nfkd_form.encode("ASCII", "ignore")
        new_text = ascii_form.decode("utf-8")

        return str(new_text)

    def format_spaces(self, text: str) -> str:
        if "  " in text:
            new_text = text.replace("  ", " ")
            return new_text

        else:
            return text

    def fix_spelling(self, text: str) -> str:
        d = dictionary()

        for k, v in d.items():
            for i in v:
                if i.lower() in text:
                    new_text = text.replace(i.lower(), k.lower())
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

    print("Running Library As Stand-Alone File...")
    input_text = input("Enter Text: ")

    s = SpellChecker()
    corrected_text = s.spell_checker(input_text)
    print("Corrected Text: " + corrected_text)
