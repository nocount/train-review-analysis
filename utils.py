# Separating out utility functions for better code cleanliness
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from collections import defaultdict
from typing import Tuple


def pretty_print_row(df, index: int):
    """
    Function for printing the contents of a review in a more readable format.

    :param df: dataframe to be printed
    :param index: row index of the dataframe that you want to print
    """
    print('Date: ' + str(df['date'].iloc[index]))
    print('Title: ' + str(df['title'].iloc[index]))
    print('Text: ' + str(df['text'].iloc[index]))
    print('URL: ' + str(df['url'].iloc[index]))
    print('Stars: ' + str(df['stars'].iloc[index]))


def extract_company(url: str):
    """
    Cleans text in url field to give distinct company url.

    :param url: string field to be stripped
    :returns: the distinct company url
    """
    company = url.split('/')[-1].split('?')[0]
    return company


def clean_rating(stars: str):
    """
    Cleans the unnecessary text from stars field to give a numeric rating.

    :param stars: rating string to be cleaned
    :returns: numeric value of rating string
    """
    rating = stars.split()[1].split('-')[-1]
    return rating


def generate_ngrams(text: str, n: int):
    """
    Creates a list of ngrams of the specified degree from a body of text.

    :param text: body of text to be broken into ngrams
    :param n: the degree of the ngram that is desired, i.e. 1 for unigrams, 2 for bigrams, etc...
    :returns: list of all ngrams in the body of text
    """
    stop = set(stopwords.words('english'))
    token = [
        token for token in text.lower().split(' ') if token not in ['-', '.', ''] if token not in stop
    ]
    ngrams = zip(*[token[i:] for i in range(n)])
    return [' '.join(ngram) for ngram in ngrams]


def plot_ngrams(df, n: int, topn: int, figsize: Tuple, color: str = u'#1f77b4'):
    """
    Plots the topn ngrams of a given dataframe.

    :param df: the dataframe to be plotted
    :param n: the degree of the ngram that is desired, i.e. 1 for unigrams, 2 for bigrams, etc...
    :param topn: the amount of ngrams to be plotted
    :param figsize: desired size of the plot
    :param color: desired color of the plot
    """
    grams = defaultdict(int)
    for comment in df['text']:
        for gram in generate_ngrams(comment, n):
            grams[gram] += 1

    grams = {k: v for k, v in sorted(grams.items(), key=lambda item: item[1], reverse=True)}
    keys = list(grams.keys())[0:topn]
    values = list(grams.values())[0:topn]

    plt.figure(figsize=figsize)
    plt.title('TopN Ngrams')
    plt.xlabel('Occurences')
    plt.ylabel('Ngram')
    plt.barh(y=keys, width=values, color=color)
    plt.gca().invert_yaxis()
