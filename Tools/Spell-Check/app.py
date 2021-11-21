import time
import pymongo
import unicodedata


def createsCorpus() -> list:
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


def stripPunctuation(text: str) -> str:
    punctuation = "!#$%'*+,./;<=>?@[\]^_`{|}~"
    new_text = text.translate(str.maketrans("", "", punctuation))

    return new_text


def stripAccents(text: str) -> str:
    nfkd_form = unicodedata.normalize("NFKD", text)
    ascii_form = nfkd_form.encode("ASCII", "ignore")
    new_text = ascii_form.decode("utf-8")

    return str(new_text)


def formatText(text: str) -> str:
    if "  " in text:
        new_text = text.replace("  ", " ")
        return new_text

    else:
        return text


def spellChecker(text: str) -> str:
    dictionary = {
        "Allah": ["allah", "allaah"],
        "Abi": ["abee"],
        "Abdul": ["abdull"],
        "Abdur": ["abdir"],
        "Abbas": ["abbaas"],
        "Aashoora": ["ashooraa"],
        "Abdullah": ["abdullaah"],
        "Abdulillah": ["abdulilah"],
        "Albani": ["albaanee", "albaani"],
        "Ansari": ["ansaree"],
        "Aqidah": ["aqeedah"],
        "Asqalani": ["asqalaani"],
        "Awiyyah": ["awiyah"],
        "Ayyan": ["ayaan"],
        "Aziz": ["azeez"],
        "Azzaam": ["azzam"],
        "Baatini": ["batinee"],
        "Baghdadi": ["baghdadee"],
        "Banna": ["bannaa"],
        "Barbahari": ["barbaharee"],
        "Bukhari": ["bukharee", "bukhaari"],
        "Buloogh": ["bulugh"],
        "Baz": ["baaz"],
        "Christmas": ["xmas"],
        "daesh": ["isis"],
        "dhahabi": ["dhahabee"],
        "eesa": ["isa", "eesaa"],
        "falasifah": ["flasafah"],
        "fatwa": ["fatwah"],
        "fawzaan": ["fawzan"],
        "imaan": ["emaan", "eemaan"],
        "Haddad": ["hadad"],
        "Hadee": ["haadee", "hadi"],
        "Haqiqiyah": ["haqeeqiyyah"],
        "Haram": ["haraam"],
        "Hassan": ["hasan"],
        "Hawadith": ["hawaadith"],
        "Hizbi": ["hizbee"],
        "Ibraheem": ["ibrahim"],
        "Idafiyyah": ["idaafiyyah"],
        "Ikhwani": ["ikhwanee", "ikhwaani"],
        "Imaam": ["imam"],
        "Imaams": ["imams"],
        "Imaan": ["iman"],
        "Islam": ["islaam"],
        "Ismaeel": ["ismael", "ismail"],
        "Istiqamah": ["istiqaamah", "istiqama"],
        "Iyaad": ["iyyadh", "iyyad"],
        "Jaabiree": ["jabiri", "jabiree"],
        "Jahmi": ["jahmee"],
        "Jamaa": ["jama"],
        "Jinn": ["jin"],
        "Kalaam": ["kalam"],
        "Kashif": ["Kashiff"],
        "Khadeejah": ["khadejah"],
        "Khawaarij": ["khawarij"],
        "Khomenei": ["khomeini"],
        "Kullab": ["kullaab"],
        "Kullabi": ["kullaabi"],
        "Kullabis": ["kullaabis"],
        "Laden": ["ladin"],
        "Luhaydan": ["luhaydaan"],
        "Madkhali": ["madkhalee"],
        "Mahdi": ["mahdee"],
        "Makhlooq": ["makhluq"],
        "Makkah": ["mecca"],
        "Maliki": ["malikee"],
        "Maryam": ["mary"],
        "Musa": ["moses"],
        "Muhamad": ["muhammad"],
        "Mutakalimeen": ["mutakalimin"],
        "Mutakalimoon": ["mutakalimun"],
        "Nabi": ["nabee", "nabiyy"],
        "Najmee": ["najmi"],
        "Naseehah": ["nasihah"],
        "Nuh": ["noah"],
        "Nuzool": ["nuzul"],
        "Umar": ["omar"],
        "Pharaoh": ["pharoah"],
        "Post codes": ["postcodes"],
        "Premier Hajj": ["premierhajj"],
        "Quran": ["quraan"],
        "Rabee": ["rabi"],
        "Ramadan": ["ramadhaan", "ramadhan"],
        "Saeed": ["saed"],
        "Safwaan": ["safwan"],
        "Sahabah": ["sahaabah"],
        "Salafi": ["salafee"],
        "Salafiyyah": ["salafiyah", "salafiyan"],
        "Salafi Publications": ["salafipublications"],
        "Salallahu": ["salallaahu"],
        "Salat": ["salaat"],
        "Salah": ["salaah"],
        "Shatibi": ["shatibee"],
        "Shayateen": ["shayaateen"],
        "Shaytaan": ["shaytan", "satan"],
        "Sharia": ["shariah"],
        "Sufyaan": ["sufyan"],
        "Sulayman": ["sulaymaan"],
        "Tadhkiratus": ["tadhkirahtus"],
        "Tafseer": ["tafsir"],
        "Taqleed": ["taqlid"],
        "Taraweeh": ["tarawih"],
        "Tawheed": ["tawhid"],
        "Ubayd": ["ubaid"],
        "Usamah": ["usaamah"],
        "Uthaymeen": ["uthaymin", "uthaimeen"],
        "Uthmaan": ["uthman"],
        "Uways": ["uwais"],
        "Wahab": ["wahhab", "wahhaab"],
        "Jihad": ["jihaad"],
        "Yahya": ["yahyaa"],
        "Zakariyyah": ["zakariyyaa", "zakariyah"],
        "Zayd": ["zaid"],
        "Zubayr": ["zubair"],
        "Zilal": ["zilaal"],
    }

    for key, values in dictionary.items():
        for i in values:
            if i.lower() in text:
                new_text = text.replace(i.lower(), key.lower())
                return new_text

            elif i.title() in text:
                new_text = text.replace(i.title(), key.title())
                return new_text

    else:
        return text


if __name__ == "__main__":

    corpus = createsCorpus()

    start = time.perf_counter()
    for i in corpus:
        text = stripPunctuation(i)
        text = stripAccents(text)
        text = formatText(text)
        text = spellChecker(text)
        print(text)

    print("")
    print("Time taken: ", time.perf_counter() - start)
    print("Items in Corpus: ", len(corpus))
