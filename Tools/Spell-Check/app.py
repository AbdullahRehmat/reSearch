from textblob import TextBlob as TB

text = "Allaah Allah Abu Khadeejah Iyaad Hakeem Taymiyyah Quraan"

text = TB(text)

textCorrected = text.correct()

print(text)
print(textCorrected)

# connect to db
# import titles as list
# for i in dict
# correct text
# save back to db in same place
# exit