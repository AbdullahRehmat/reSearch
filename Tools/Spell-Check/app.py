import time
import pymongo
import unicodedata


def createsCorpus():
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


def stripPunctuation(text):
    punctuation = "!#$%'*+,./;<=>?@[\]^_`{|}~"
    new_text = text.translate(str.maketrans("", "", punctuation))

    return new_text


def stripAccents(text):
    nfkd_form = unicodedata.normalize("NFKD", text)
    ascii_form = nfkd_form.encode("ASCII", "ignore")
    new_text = ascii_form.decode("utf-8")

    return str(new_text)


def formatText(text):
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
        "albani": ["albaanee", "albaani"],
        "ansari": ["ansaree"],
        "aqidah": ["aqeedah"],
        "asqalani": ["asqalaani"],
        "awiyyah": ["awiyah"],
        "ayyan": ["ayaan"],
        "aziz": ["azeez"],
        "azzaam": ["azzam"],
        "baatini": ["batinee"],
        "baghdadi": ["baghdadee"],
        "banna": ["bannaa"],
        "barbahari": ["barbaharee"],
        "bukhari": ["bukharee", "bukhaari"],
        "buloogh": ["bulugh"],
        "Baz": ["baaz"],
        "christmas": ["xmas"],
        "daesh": ["isis"],
        "dhahabi": ["dhahabee"],
        "eesa": ["isa", "eesaa"],
        "falasifah": ["flasafah"],
        "fatwa": ["fatwah"],
        "Fawzaan": ["fawzan"],
        "imaan": ["emaan", "eemaan"],
        "haddad": ["hadad"],
        "hadee": ["haadee", "hadi"],
        "haqiqiyah": ["haqeeqiyyah"],
        "haram": ["haraam"],
        "hassan": ["hasan"],
        "hawadith": ["hawaadith"],
        "hizbi": ["hizbee"],
        "ibraheem": ["ibrahim"],
        "idafiyyah": ["idaafiyyah"],
        "ikhwani": ["ikhwanee", "ikhwaani"],
        "imaam": ["imam"],
        "imaams": ["imams"],
        "imaan": ["iman"],
        "islam": ["islaam"],
        "ismaeel": ["ismael", "ismail"],
        "istiqamah": ["istiqaamah", "istiqama"],
        "Iyyad": ["iyyadh"],
        "Jaabiree": ["jabiri", "jabiree"],
        "Jahmi": ["jahmee"],
        "jamaa": ["jama"],
        "Jinn": ["jin"],
        "kalaam": ["kalam"],
        "Kashif": ["Kashiff"],
        "Khadeejah": ["khadejah"],
        "khawaarij": ["khawarij"],
        "Khomenei": ["khomeini"],
        "kullab": ["kullaab"],
        "kullabi": ["kullaabi"],
        "kullabis": ["kullaabis"],
        "laden": ["ladin"],
        "Luhaydan": ["luhaydaan"],
        "Madkhali": ["madkhalee"],
        "Mahdi": ["mahdee"],
        "makhlooq": ["makhluq"],
        "Makkah": ["mecca"],
        "Maliki": ["malikee"],
        "Maryam": ["mary"],
        "Musa": ["moses"],
        "Muhamad": ["muhammad"],
        "mutakalimeen": ["mutakalimin"],
        "mutakalimoon": ["mutakalimun"],
        "nabi": ["nabee", "nabiyy"],
        "Najmee": ["najmi"],
        "naseehah": ["nasihah"],
        "Nuh": ["noah"],
        "nuzool": ["nuzul"],
        "Umar": ["omar"],
        "Pharaoh": ["pharoah"],
        "post codes": ["postcodes"],
        "Premier Hajj": ["premierhajj"],
        "Quran": ["quraan"],
        "Rabee": ["rabi"],
        "ramadan": ["ramadhaan", "ramadhan"],
        "Saeed": ["saed"],
        "Safwaan": ["safwan"],
        "Sahabah": ["sahaabah"],
        "salafi": ["salafee"],
        "salafiyyah": ["salafiyah", "salafiyan"],
        "Salafi Publications": ["salafipublications"],
        "salallahu": ["salallaahu"],
        "salat": ["salaat"],
        "salah": ["salaah"],
        "Shatibi": ["shatibee"],
        "Shayateen": ["shayaateen"],
        "Shaytaan": ["shaytan", "satan"],
        "sharia": ["shariah"],
        "Sufyaan": ["sufyan"],
        "Sulayman": ["sulaymaan"],
        "tadhkiratus": ["tadhkirahtus"],
        "tafseer": ["tafsir"],
        "taqleed": ["taqlid"],
        "taraweeh": ["tarawih"],
        "tawheed": ["tawhid"],
        "Ubayd": ["ubaid"],
        "Usamah": ["usaamah"],
        "Uthaymeen": ["uthaymin", "uthaimeen"],
        "Uthmaan": ["uthman"],
        "Uways": ["uwais"],
        "Wahab": ["wahhab", "wahhaab"],
        "jihad": ["jihaad"],
        "Yahya": ["yahyaa"],
        "Zakariyyah": ["zakariyyaa", "zakariyah"],
        "Zayd": ["zaid"],
        "Zubayr": ["zubair"],
        "zilal": ["zilaal"],
    }

    for key, values in dictionary.items():
        for i in values:
            if i in text.lower:
                new_text = text.replace(i, key)
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
    print(time.perf_counter() - start)
