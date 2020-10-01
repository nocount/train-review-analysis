# Separating out utility functions for better code cleanliness
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from collections import defaultdict


def pretty_print_row(df, index: int):
    print('Date: ' + str(df['date'].iloc[index]))
    print('Title: ' + str(df['title'].iloc[index]))
    print('Text: ' + str(df['text'].iloc[index]))
    print('URL: ' + str(df['url'].iloc[index]))
    print('Stars: ' + str(df['stars'].iloc[index]))
    
    
def extract_company(url: str):
    company = url.split('/')[-1].split('?')[0]
    return company


def clean_rating(stars: str):
    rating = stars.split()[1].split('-')[-1]
    return rating


def create_corpus(df):
    corpus = []
    for row in df['text']:
        for word in row.split():
                corpus.append(word.lower())
            
    return corpus


def generate_ngrams(text: str, n: int):
    stop = set(stopwords.words('english'))
    token = [token for token in text.lower().split(' ') if token != '' if token not in stop]
    ngrams = zip(*[token[i:] for i in range(n)])
    return [' '.join(ngram) for ngram in ngrams]


def plot_ngrams(df, n, topn, figsize):
    grams = defaultdict(int)
    for comment in df['text']:
        for gram in generate_ngrams(comment, n):
            grams[gram] += 1

    grams = {k: v for k, v in sorted(grams.items(), key=lambda item: item[1], reverse=True)}

    keys = list(grams.keys())[0:topn]
    values = list(grams.values())[0:topn]
    plt.figure(figsize=figsize)
    plt.barh(y=keys, width=values)
    plt.gca().invert_yaxis()