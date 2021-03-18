from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

print(ps.stem("e"))