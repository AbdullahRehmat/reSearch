import pymongo
import unicodedata
from wordlist import dictionary


class SpellChecker():
    def __init__(self) -> None:
        pass

    # @classmethod
    # def create_corpus_db() -> list:
    #    host = "localhost"  # Mongo-CS
    #    port = 27019
    #    db_name = "ContentScraperDB"
    #    col_name = "ScrapedDataC1"
    #
    #    conn = pymongo.MongoClient(host=f"mongodb://{host}:{str(port)}/")
    #
    #    db = conn[db_name]
    #    col = db[col_name]
    #
    #    corpus = []
    #    for data in col.find():
    #        corpus += data["title"]
    #
    #    return corpus
    @classmethod
    def strip_punctuation(self, text: str) -> str:
        punctuation = "!#$%'*+,./;<=>?@[\]^_`{|}~"
        new_text = text.translate(str.maketrans("", "", punctuation))

        return new_text

    @classmethod
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

    @classmethod
    def fix_spelling(self, text: str) -> str:
        d = dictionary()

        for key, values in d.items():
            for i in values:
                if i.lower() in text:
                    new_text = text.replace(i.lower(), key.lower())
                    return new_text

                elif i.title() in text:
                    new_text = text.replace(i.title(), key.title())
                    return new_text

        else:
            return text

    def spell_checker(self, text: str) -> str:

        # Split Text -> Words
        words = text.split(" ")
        x = []

        # Spell Check Words
        for word in words:
            word = self.strip_punctuation(word)
            word = self.strip_accents(word)
            word = self.format_spaces(word)
            word = self.fix_spelling(word)

            x.append(word)

        # Join Words -> Sentence
        sentence = " "
        sentence = sentence.join(x)

        # Return Sentence
        return sentence


if __name__ == "__main__":

    print("Running Library As Stand-Alone File...")
    s = SpellChecker()
    new_text = s.spell_checker("abdullaah allaah noah")
    print(new_text)
