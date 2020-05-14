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
        df_schedule = df[x * 2 + 1]
        df_title = df[x * 2]

        # try:
        # df_title.rename(columns=df_title.iloc[0], inplace=True)

        # Changed to index drop 1 because of their change in format of website
        try:
            df_title = df_title.reindex(df_title.index.drop(1))
        except KeyError:
            continue
        
        df_title = df_title[0][0]

        if isinstance(store.get(df_title), pd.DataFrame) and not store[df_title].empty: # Terminate early if already stored
            continue

        store[df_title] = df_schedule
        print(df_title)
        # print(df_schedule)
    # print(store)

    with open('allscheduledict.p', 'wb') as f:
        pickle.dump(store, f)
