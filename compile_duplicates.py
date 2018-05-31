import pandas as pd
import numpy as np
import pickle

tables = {}

with open('allscheduledict.p', 'rb') as f:
    tables = pickle.load(f)

for key in tables.keys():
    table = tables[key]
    indexes = list(table['INDEX'])
    indexes = list(filter(lambda v: v == v, indexes))
    table['INDEX'].fillna(method='ffill', inplace=True)

    table_index = {}
    for index in indexes:
        table_index[index] = table[table['INDEX'] == index]

    combined_table = pd.DataFrame()
    for idx, index in enumerate(indexes):
        if index not in table_index.keys():
            continue
        for x in range(idx + 1, len(indexes)):
            if indexes[x] not in table_index.keys():
                continue
            if np.array_equal(np.array(table_index[index]['DAY']),
                              np.array(table_index[indexes[x]]['DAY'])) and np.array_equal(np.array(
                    table_index[index]['TIME']), np.array(table_index[indexes[x]]['TIME'])):
                table_index[index]['INDEX'] = np.array(table_index[index]['INDEX']) + '|' + np.array(
                    table_index[indexes[x]]['INDEX'])
                table_index[index]['GROUP'] = np.array(table_index[index]['GROUP']) + '|' + np.array(
                    table_index[indexes[x]]['GROUP'])
                del table_index[indexes[x]]

        if combined_table.empty:
            combined_table = table_index[index]
        else:
            combined_table = combined_table.append(table_index[index])
    tables[key] = combined_table

with open('compiledscheduledict.p', 'wb') as f:
    pickle.dump(tables, f)

