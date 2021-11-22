import pymongo
import unicodedata
from wordlist import dictionary


class SpellChecker():
    def __init__(self) -> None:
        pass

    def create_corpus_db(self) -> list:
        host = "localhost"  # Mongo-CS
        port = 27019
        db_name = "ContentScraperDB"
        col_name = "ScrapedDataC1"

        conn = pymongo.MongoClient(host=f"mongodb://{host}:{str(port)}/")

        db = conn[db_name]
        col = db[col_name]

        corpus = []
        for data in col.find():
            corpus += data["title"]

        return corpus

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

    def spell_checker_text(self, text: str) -> str:
        text = self.strip_punctuation(text)
        text = self.strip_accents(text)
        text = self.format_spaces(text)
        text = self.fix_spelling(text)

        text = str(text)

        return text

    def spell_checker_db(self) -> list:
        corpus = self.create_corpus_db()

        for text in corpus:
            text = self.strip_punctuation(text)
            text = self.strip_accents(text)
            text = self.format_spaces(text)
            text = self.fix_spelling(text)
            new_corpus = text

        return new_corpus


if __name__ == "__main__":

    print("Running Library As Stand-Alone File...")
    checked_text = SpellChecker.spell_checker_db()
    print(checked_text)
