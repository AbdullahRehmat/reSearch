from textblob import TextBlob as TB

text = "being-thankful-to-allaah-by-abu-fudhayl"

text = TB(text)

textCorrected = text.correct()

print(type(textCorrected))
print(textCorrected)

# connect to db
# import titles as list
# for i in dict
# correct text
# save back to db in same place
# exit