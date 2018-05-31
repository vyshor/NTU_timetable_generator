import pickle

tables = {}

with open('compiledscheduledict.p', 'rb') as f:
    tables = pickle.load(f)

DATA = {}

# print(list(tables.keys()))
# exit()
for coursecode in tables.keys():
    table = tables[coursecode]
    DATAmini = {}
    if not table.empty:
        indexes = set(table['INDEX'])
        for index in indexes:
            DATAmini[index] = []
            tablemini = table[table['INDEX'] == index]
            for row in tablemini.itertuples(index=False, name=None):
                to_append = list(filter(lambda v: v == v, row))
                to_append[-1] = to_append[-1].replace('Teaching ', "")
                DATAmini[index].append(to_append[1:])

        DATA[coursecode] = DATAmini

with open('database.p', 'wb') as f:
    pickle.dump(DATA, f)