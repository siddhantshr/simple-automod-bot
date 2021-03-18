from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
import asyncio

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

async def strip_chars(string: str):
    new_string = ''.join(c for c in string if c.isalpha())
    return new_string

async def remove_unicode_chars(word: str):
    string_encode = word.encode("ascii", "ignore")
    decoded = string_encode.decode()
    return decoded

async def get_root_form(word: str):
    word = word.lower()
    word = word.replace(" ", "")
    word = word.replace("z", "s")
    word = await strip_chars(word)
    word = await remove_unicode_chars(word)
    word = lemmatizer.lemmatize(word)
    word = ps.stem(word)

    return word

async def get_lemmatized_sentence(sentence: str):
    sentence = sentence.strip()
    words = sentence.split(" ")
    
    for idx, x in enumerate(words):
        words[idx] = await get_root_form(x)

    for idx, x in enumerate(words):
        if x == "":
            words.pop(idx)

    return tuple(words)

# if __name__ == "__main__":
#     print(asyncio.run(get_lemmatized_sentence("DMSDMKM hehehe HRU doing l😆 im doing poggers")))