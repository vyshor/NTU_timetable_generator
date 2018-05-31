import pandas as pd
import pickle
import os.path


def extract_table(html):
    try:
        df = pd.read_html(html)
    except ValueError:
        print("No tables found in this section")
        return

    store = {}

    if os.path.isfile('allscheduledict.p'):
        with open('allscheduledict.p', 'rb') as f:
            store = pickle.load(f)

    for x in range(len(df) // 2):
        df_title = df[x * 2 + 1]
        df_schedule = df[x * 2]

        df_title.rename(columns=df_title.iloc[0], inplace=True)
        df_title = df_title.reindex(df_title.index.drop(0))
        store[df_schedule[0][0]] = df_title

    with open('allscheduledict.p', 'wb') as f:
        pickle.dump(store, f)
