import pandas as pd
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
  
class TwitterClient(object):

    def __init__(self):

        # Keys y tokens de twitter
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
  
        # intenta autenticacion
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Autenticacion Fallida")
  
    def clean_tweet(self, tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
  
    def get_tweet_sentiment(self, tweet):

        # crear un objeto TextBlob con el texto del tweet
        analisis = TextBlob(self.clean_tweet(tweet))
        # clasificar sentimiento
        if analisis.sentiment.polarity > 0:
            return 'positivo'
        elif analisis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negativo'
  
    def get_tweets(self, query, count = 10):

        # lista vacia para guardar tweets
        tweets = []
  
        try:
            # llama a la api de twitter para buscar tweets
            tweets_buscados = self.api.search(q = query, count = count)
  
            # parsear los tweets uno por uno
            for tweet in tweets_buscados:
                # diccionario vacio para guardar los parametros requeridos de un tweet
                tweets_parseados = {}
  
                # guardar el texto
                tweets_parseados['texto'] = tweet.text
                # guardar el sentimiento
                tweets_parseados['sentimiento'] = self.get_tweet_sentiment(tweet.text)
  
                # añadir el tweet analizado a la lista de tweets
                if tweet.retweet_count > 0:
                    # si el tweet tiene retweets se asegura de que se añade solo una vez
                    if tweets_parseados not in tweets:
                        tweets.append(tweets_parseados)
                else:
                    tweets.append(tweets_parseados)
  
            # devuelve los tweets parseados
            return tweets
  
        except tweepy.TweepError as e:
            print("Error : " + str(e))
  
def main():
    
    df_comb = pd.read_csv("df_combinada.csv")
    # llama a la funcion de capturar tweets
    tweets = df_comb.iloc[:,3]
  
    # selecciona los tweets positivos de la lista
    ptweets = [tweet for tweet in tweets if tweet['sentimiento'] == 'positivo']
    # porcentaje de tweets Positivos
    print("Porcentaje de tweets Positivos: {} %".format(100*len(ptweets)/len(tweets)))
    
    # selecciona los tweets negativos de la lista
    ntweets = [tweet for tweet in tweets if tweet['sentimiento'] == 'negativo']
    # porcentaje de tweets Negativos
    print("Porcentaje de tweets Negativos: {} %".format(100*len(ntweets)/len(tweets)))
    
    # porcentaje de tweets Neutros
    print("Porcentaje de tweets Neutros: {} % \
        ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
  
    # Imprime los 5 primeros tweets positivos
    print("\n\nTWEETS POSITIVOS:")
    for tweet in ptweets[:5]:
        print("\nTexto: ")
        print(tweet['texto'])
  
    # Imptime los 5 primeros tweets negativos
    print("\n\nTWEETS NEGATIVOS:")
    for tweet in ntweets[:5]:
        print("\nTexto: ")
        print(tweet['texto'])
  
if __name__ == "__main__":
    # llama a la funcion main
    main()
