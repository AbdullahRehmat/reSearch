from rank_bm25 import BM25Okapi, BM25L, BM25Plus


corpus = ['The Clinic: How Psychologically Insecure Atheists Comfort Themselves - Part 1', 'The Shia of Kufah Deceived, Deserted, Ambushed and Murdered the Grandson of the Prophet Al-Husayn, His Brothers and His Children and Took Their Women as Captives', 'The Shia Believe Revelation Continued After the Messenger and the Saying of Their Imaams Is the Saying of Allaah', "The Virtues of Aa'ishah Al-Siddiqah, Daughter of Abu Bakr: Part 3 - A Scholar for the Companions", 'A Revealing Glimpse at the Doctrines of the Nusayriyyah (Alawi) Sect', "Kuwaiti Rafidi Yasir Al-Habib: Celebrating the Death of Aa'ishah Al-Siddiqah", 'Uncovering the Hidden Realities of Hizbollah: Part 5 - The Hoothees in Yemen', 'Tafsir of Furat Al-Kufi: The Understanding of Shirk With the Shia (And Why Sunnis Are Considered Mushriks)', "The Virtues of Aa'ishah Al-Siddiqah, Daughter of Abu Bakr: Part 2", "The Virtues of Aa'ishah Al-Siddiqah, Daughter of Abu Bakr: Part 1 ", 'The Ahl Al-Bayt Were Harmed, Grieved and Also Killed by the Shia of Al-Kufah', "More Shi'ite Authorities on the Existence and Reality of Abdullah Bin Saba'", 'Kuwaiti Rafidi Yasir Al-Habib: All Children Are Offspring of Fornication (Born of Prostitutes) Except Those of the Shia', 'Uncovering the Hidden Realities of Hizbollah: Part 4 -  Iranian Rafidi Shia Proxies in Other Lands - Saudi Arabia',
          'Uncovering the Hidden Realities of Hizbollah: Part 3 - Iranian Rafidi Shia Proxies in Other Lands - Bahrain', 'Uncovering the Hidden Realities of Hizbollah: Part 2 - The Doctrines and Beliefs of the Founders of Hizbollah', 'The Virtues of Abu Bakr Al-Siddeeq: Part 3 - Three Distinct Excellences of Abu Bakr Not Shared By Anyone Else', 'The Virtues of Abu Bakr Al-Siddeeq: Part 2 - Abu Bakr in The Quran', 'The Virtues of Abu Bakr Al-Siddeeq: Part 1 - His Lineage and Titles', 'Uncovering the Hidden Realities of Hizbollah: Part 1 - Origins and Formation of the Group', "Muhammad Al-Kashi (d. 340H) Early Shi'ite Authority on Abdullah Bin Saba' Al-Yahudi and the Origins of the Rafidi Shia Sect", 'Al-Tabarsi: Seeking Aid, Rescue, Deliverance by Supplicating Directly to the Messenger and to Alee', "A Brief Overview of the Doctrines Innovated by Abdullah Bin Saba' Al-Yahudi Which Became the Foundational Beliefs of the Sects of the Shia", "Affirmation From Shia Source Books That Abdullah Bin Saba' Is the Original Founder of Rafidi Shia Doctrines", "Al-Naubakhti and Al-Qummee (3rd Century Hijrah Shia Scholars): Founder of Major Shia Doctrines Is Abdullah Bin Saba' Al-Yahudi", 'Ayat Al-Shaytan Khomeini: Seeking Aid From the Dead (And Stones and Mud)  Is Not Shirk ', 'Understanding and Classifying the Various Shia Sects']

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Plus(tokenized_corpus)

query = "Uncovering the Hidden"

tokenized_query = query.split(" ")
doc_scores = bm25.get_scores(tokenized_query)
results = bm25.get_top_n(tokenized_query, corpus, n=10)


#print(len(corpus))
print(doc_scores)
#print('\n'.join(results))

"""
BM25Plus
BM25L
BM25Okapi
"""