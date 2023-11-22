import tweepy
from tweepy import OAuthHandler
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import TweetTokenizer
import matplotlib.pyplot as plt
import pandas as pd
import re



def clean_text(text):
    # Eliminar enlaces
    text = re.sub(r'http\S+', '', text)
    # Eliminar menciones
    text = re.sub(r'@\S+', '', text)
    # Eliminar caracteres especiales y números
    text = re.sub(r'[^A-Za-z\s]', '', text)
    return text



# Configuración de las claves de API de Twitter
consumer_key = '' 
consumer_secret = '' 
access_token = '' 
access_secret = ''

# 1722792559443902464-jjGGAuq8NEPpxFaBHiXTNlrtweB75R
# tJSnVcSlKtphlvB3PP1DH1a3QOBPxq17k2J9yhLPXxAck

# Autenticación con la API de Twitter
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Ubicación geográfica para la búsqueda de tweets relacionados con Guatemala
"""geocode = "15.7835,-90.2308,500km"  # Latitud, longitud y radio (en kilómetros) alrededor de Guatemala"""

# Recopilar tweets relacionados con Guatemala
"""tweets = tweepy.Cursor(api.search_tweets, q="", geocode=geocode, lang="es", tweet_mode='extended').items(10000)"""



# Cargar datos desde el archivo CSV
df = pd.read_csv('AllTweets.csv') 
#tweets = df['text'].tolist()

# Eliminar filas con tweets nulos
df = df.dropna(subset=['text'])

# Aplicar la función de limpieza a cada tweet
df['cleaned_tweet'] = df['text'].apply(clean_text)
tweets = df['cleaned_tweet'].tolist()

# Tokenización utilizando TweetTokenizer
#tokenizer = TweetTokenizer()
#df['tokenized_tweet'] = df['cleaned_tweet'].apply(tokenizer.tokenize)
#tweets = df['tokenized_tweet'].tolist()


# Descargar las stopwords en inglés 
nltk.download('stopwords')
nltk.download('punkt')

# Preprocesamiento de texto
#stop_words = set(stopwords.words('spanish'))
stop_words = list(stopwords.words('english'))
filtered_tweets = []

# Se añade la stoprword: amp, ax, ex
stop_words.extend(("us", "like", "rt", "get", "via", "new", "day", "watch", "im","see", "dont", "good", "make"))
#print(stop_words[:10])
        

        
for tweet in tweets:
    words = word_tokenize(tweet.lower())  # Tokenización y conversión a minúsculas
    filtered_tweet = [word for word in words if word.isalnum() and word not in stop_words]  # Eliminación de stopwords y caracteres especiales
    filtered_tweets.extend(filtered_tweet)

# Análisis de frecuencia de palabras
frecuencia = FreqDist(filtered_tweets)
frecuencia.plot(20, cumulative=False)  # Mostrar las 20 palabras más frecuentes
#plt.show()
