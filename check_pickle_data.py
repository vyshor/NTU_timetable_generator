import pandas as pd
import pickle
import os.path

if os.path.isfile('database.p'):
    with open('database.p', 'rb') as f:
        store = pickle.load(f)

print(store.keys())
print([x for x in store.keys() if 'CZ' in x])

print(store['HE9091'])	