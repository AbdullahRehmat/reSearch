import json
from rank_bm25 import BM25Okapi, BM25L, BM25Plus
"""

query = "uncovering the hidden"

corpus = ['The Clinic: How Psychologically Insecure Atheists Comfort Themselves - Part 1', 'The Shia of Kufah Deceived, Deserted, Ambushed and Murdered the Grandson of the Prophet Al-Husayn, His Brothers and His Children and Took Their Women as Captives', 'The Shia Believe Revelation Continued After the Messenger and the Saying of Their Imaams Is the Saying of Allaah', "The Virtues of Aa'ishah Al-Siddiqah, Daughter of Abu Bakr: Part 3 - A Scholar for the Companions", 'A Revealing Glimpse at the Doctrines of the Nusayriyyah (Alawi) Sect', "Kuwaiti Rafidi Yasir Al-Habib: Celebrating the Death of Aa'ishah Al-Siddiqah", 'Uncovering the Hidden Realities of Hizbollah: Part 5 - The Hoothees in Yemen', 'Tafsir of Furat Al-Kufi: The Understanding of Shirk With the Shia (And Why Sunnis Are Considered Mushriks)', "The Virtues of Aa'ishah Al-Siddiqah, Daughter of Abu Bakr: Part 2", "The Virtues of Aa'ishah Al-Siddiqah, Daughter of Abu Bakr: Part 1 ", 'The Ahl Al-Bayt Were Harmed, Grieved and Also Killed by the Shia of Al-Kufah', "More Shi'ite Authorities on the Existence and Reality of Abdullah Bin Saba'", 'Kuwaiti Rafidi Yasir Al-Habib: All Children Are Offspring of Fornication (Born of Prostitutes) Except Those of the Shia', 'Uncovering the Hidden Realities of Hizbollah: Part 4 -  Iranian Rafidi Shia Proxies in Other Lands - Saudi Arabia',
          'Uncovering the Hidden Realities of Hizbollah: Part 3 - Iranian Rafidi Shia Proxies in Other Lands - Bahrain', 'Uncovering the Hidden Realities of Hizbollah: Part 2 - The Doctrines and Beliefs of the Founders of Hizbollah', 'The Virtues of Abu Bakr Al-Siddeeq: Part 3 - Three Distinct Excellences of Abu Bakr Not Shared By Anyone Else', 'The Virtues of Abu Bakr Al-Siddeeq: Part 2 - Abu Bakr in The Quran', 'The Virtues of Abu Bakr Al-Siddeeq: Part 1 - His Lineage and Titles', 'Uncovering the Hidden Realities of Hizbollah: Part 1 - Origins and Formation of the Group', "Muhammad Al-Kashi (d. 340H) Early Shi'ite Authority on Abdullah Bin Saba' Al-Yahudi and the Origins of the Rafidi Shia Sect", 'Al-Tabarsi: Seeking Aid, Rescue, Deliverance by Supplicating Directly to the Messenger and to Alee', "A Brief Overview of the Doctrines Innovated by Abdullah Bin Saba' Al-Yahudi Which Became the Foundational Beliefs of the Sects of the Shia", "Affirmation From Shia Source Books That Abdullah Bin Saba' Is the Original Founder of Rafidi Shia Doctrines", "Al-Naubakhti and Al-Qummee (3rd Century Hijrah Shia Scholars): Founder of Major Shia Doctrines Is Abdullah Bin Saba' Al-Yahudi", 'Ayat Al-Shaytan Khomeini: Seeking Aid From the Dead (And Stones and Mud)  Is Not Shirk ', 'Understanding and Classifying the Various Shia Sects']


def uppercase(corpus, query):
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Plus(tokenized_corpus)

    query = query.title()

    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    results = bm25.get_top_n(tokenized_query, corpus, n=5)
    print("Uppercase Query: " + query)
    print(doc_scores)
    print('\n'.join(results))


def lowercase(corpus, query):
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Plus(tokenized_corpus)

    query = query.lower()

    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    results = bm25.get_top_n(tokenized_query, corpus, n=5)
    print("Lowercase Query: " + query)
    print(doc_scores)
    print('\n'.join(results))

uppercase(corpus, query)
lowercase(corpus, query)
"""

test = {"test":"[\"<a href=\\\"http://www.asharis.com/creed/articles/jchtj-ashari-competition-corner-2nd-quiz---did-allaah-speak-with-anything-that-negates.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Ash'ari Competition Corner: 2nd Quiz - Did Allaah Speak With Anything That Negates His Truthfulness? Test Your Understanding of 'Kalaam Nafsee' and Take Your Ash'ariyyah For A Challenging Test Drive</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/beyyw-ashari-competition-corner-1st-quiz---test-your-knowledge-of-jismiyyah.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Ash'ari Competition Corner: 1st Quiz - Test Your Knowledge of Jismiyyah</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/tagwt-jahmite-intellectual-fraudsters-abu-bilal-maliki-faqir-and-muhammad-fahmi-on-the.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Jahmite Intellectual Fraudsters Abu Bilal Maliki, Faqir, and Muhammad Fahmi on the Authorship of al-Ibanah by Abu al-Hasan al-Ash'ari - Part 8: Hanafi Tamperings of al-Ibanah</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/bkual-the-ashari-creed-and-20th-century-thinkers-and-political-activists-part-2d---the.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">The Ash'ari Creed and 20th Century Thinkers and Political Activists: Part 2d - The Aqidah of Taqi ud-Din an-Nabahani: It is Haraam to Have I'tiqaad (Belief) in the Punishment of the Grave</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/kmojk-the-ashari-creed-and-20th-century-thinkers-and-political-activists-part-2e---the.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">The Ash'ari Creed and 20th Century Thinkers and Political Activists: Part 2e - The Aqidah of Taqi ud-Din an-Nabahani: The Aqidah of the Jahmiyyah, Mu'tazilah and Ash'ariyyah that the Qur'an is Created</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/otpgh-the-ashari-creed-and-20th-century-thinkers-and-political-activists-part-2f---the.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">The Ash'ari Creed and 20th Century Thinkers and Political Activists: Part 2f - The Aqidah of Taqi ud-Din an-Nabahani: an-Nabahani and the Bid'ah of the Qadariyyah - First Installment</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/guabk-the-ashari-creed-and-20th-century-thinkers-and-political-activists-part-2g---the.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">The Ash'ari Creed and 20th Century Thinkers and Political Activists: Part 2g - The Aqidah of Taqi ud-Din an-Nabahani: an-Nabahani and the Bid'ah of the Qadariyyah - Second Installment </a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/uywlc-the-ashari-creed-and-20th-century-thinkers-and-political-activists-part-2h---the.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">The Ash'ari Creed and 20th Century Thinkers and Political Activists: Part 2h - The Aqidah of Taqi ud-Din an-Nabahani: an-Nabahani and the Bid'ah of the Qadariyyah - Third Installment </a><br />\", \"<a href=\\\"http://www.mutazilah.com/articles/udxtyrc-a-broad-outline-of-the-mutazilah-sect.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">A Broad Outline of the Mu'tazilah Sect</a><br />\", \"<a href=\\\"http://www.mutazilah.com/articles/towiuhy-shaykh-muhammad-amaan-al-jaamee-the-mutazilah-are-present-today-the-shiah-ibaadiyyah.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Shaykh Muhammad Amaan al-Jaamee: The Mu'tazilah Are Present Today (the Shi'ah, Ibaadiyyah)</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/gvutg-jahmite-intellectual-fraudster-abdullah-ali-al-amin-nur-uz-zaman-institute-phila.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Jahmite Intellectual Fraudster Abdullah Ali al-Amin (Nur uz-Zaman Institute, Philadelphia) Refuted by al-Baqillani, al-Bayhaqi and Early Kullaabi Ash'aris</a><br />\", \"<a href=\\\"http://www.asharis.com/creed/articles/vncoz-the-ashari-creed-and-20th-century-thinkers-and-political-activists-part-2i---the.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">The Ash'ari Creed and 20th Century Thinkers and Political Activists: Part 2i - The Aqidah of Taqi ud-Din an-Nabahani: The Bid'ah of the Murji'ah</a><br />\", \"<a href=\\\"http://piousmuslim.com/articles/fibunaf-saeed-bin-jubayr-what-is-khashyah-awe-of-allaah.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Sa'eed Bin Jubayr: What Is Khashyah (Awe of Allaah)?</a><br />\", \"<a href=\\\"http://www.islamagainstextremism.com/articles/uwsxqxq-ideological-roots-of-the-london-bridge-killer-usman-khan.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Ideological Roots of the London Bridge Killer, Usman Khan</a><br />\", \"<a href=\\\"http://www.mutazilah.com/articles/gswrrmz-sayyid-ahmad-khn-and-markazi-jamiat-e-ahle-hadees-hind.cfm\\\" class=\\\"searchResult\\\" target=\\\"_blank\\\" rel=\\\"noopener noreferrer\\\">Neo-Mu'tazili Sayyid Ahmad Khan and Markazi Jamiat-E-Ahle Hadees Hind</a><br />\"]"}
test = test["test"]
test = json.loads(test)

print(type(test))

for i in test:
    print(i)