from nltk.tokenize import word_tokenize
# from nltk.tokenize import sent_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import random
import string
# import pickle

fac = StemmerFactory()
stemmer = fac.create_stemmer()

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')



def normalisasi(kalimat):
    return word_tokenize(kalimat.translate(str.maketrans('','', string.punctuation)).lower())

input_salam = ('halo', 'hi', 'hallo', 'hai', 'hey')
output_salam = ('hai', 'hallo', 'hey', 'Selamat datang di chatbot warkop!')

def salam(slm):
  for i in slm.split():
    if i.lower() in input_salam:
      return random.choice(output_salam)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

def jawab(user, token_kalimat):
  respon=''

  vec = TfidfVectorizer(tokenizer= normalisasi, stop_words = set(stopwords.words('indonesian')))
  tfidf = vec.fit_transform(token_kalimat)
  same = cosine_similarity(tfidf[-1], tfidf)
  index = same.argsort()[0][-2]
  flat = same.flatten()
  flat.sort()
  frek = flat[-1]

  if (frek < 0):
    respon = respon + 'maaf, saya tidak paham pertanyaan anda'
    return respon

  else:
    respon = respon + token_kalimat[index]
    return respon


def proses_jawaban(txt, token_kalimat, token_kata):
  user = txt.lower()
  if (user != 'keluar'):
    if (user == 'terima kasih' or user == 'terimakasih' or user == 'thanks' or user == 'thank you'):
      jawab_bot = 'sama-sama'
    else:
      if (salam(user) != None):
          jawab_bot = salam(user)
      else:
        user = stemmer.stem(user)
        token_kalimat.append(user)
        token_kata = token_kata + word_tokenize(user)
        jawab_bot = jawab(user, token_kalimat)
        token_kalimat.remove(user)
  else:
    jawab_bot = "BOT: Selamat tinggal! Terima Kasih."
  return jawab_bot