# Anal;yzing train comments I guess

import pandas as pd
import numpy as np

df = pd.read_json('./data/train_reviews.json')
print(df.head())
print(df.columns)

print(df['stars'].value_counts())