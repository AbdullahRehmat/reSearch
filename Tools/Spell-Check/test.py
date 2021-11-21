test = {
    "Allah": ["allah", "Allaah", "allaah"],
    "Abdullah": ["abdullah", "Abdullaah", "abdullaah"]
}


def spellChecker(text: str):
    for key, values in test.items():
        for i in values:
            if i in text:
                new_text = text.replace(i, key)
                return new_text
            
    else:
        return text

if __name__ == "__main__":

    incorrect_text = "abdullah wrote this"
    print(spellChecker(incorrect_text))

    incorrect_text = "Abdullaah wrote this"
    print(spellChecker(incorrect_text))

    incorrect_text = "abdullaah wrote this"
    print(spellChecker(incorrect_text))