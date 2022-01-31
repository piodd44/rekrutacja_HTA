import numpy as np

expected_name_1 = ['oznaczenie zadania', 'tytuł zadania', 'lp', 'opis', 'inn', 'postać', 'opakowanie', 'dawka', 'moc',
                   'ilość',
                   'jednostki', 'inne']

list_opakowanie = ["tabl.", "tabl", "fiol", "flakon", "strz", "amp.", "amp", "fiol.", "worek", "kaps", "kaps.", "poj",
                   "poj.", "op.", "op", "but", "but.", "butelka", "ampułka", "ampulka", "tabletka"]
"można spróbować zrobić słownik dla kolumn i " \
"potem zliczać słowa pasujące do kolumny" \
" i w ten sposób decydowac która to jest kolumna"
"słownik zrobić z pewnych danych"


class ColumnClassifier:
    def __init__(self, data_frame):
        "tu bedziemy zliczac wystapienia"
        self.dict_of_set = {}
        self.names_list = []
        self.make_dictionary(data_frame)
        self.counter_for_columns(data_frame)

    def get_columns_name(self):
        pass

    def make_standard_string(self, before):
        result = str(before)
        result = result.lower().strip()
        return result

    "idea taka by dopasować możliwe najlepsze kolumny"

    def counter_for_columns(self, data_frame):
        all_counter_list = []
        for column in data_frame:
            counter_list = [0 for x in self.names_list]
            list_row_in_col = data_frame[column]
            len_of_all_row = 0
            for row in list_row_in_col:
                standard = self.make_standard_string(row)
                words_in_row = standard.split()
                len_of_all_row += len(words_in_row)
                for word in words_in_row:
                    standard = self.make_standard_string(word)
                    if standard == "nan":
                        len_of_all_row -= 1
                        break
                    for i, name in enumerate(self.names_list):
                        if standard in self.dict_of_set[name]:
                            counter_list[i] += 1
            avg_len = (len_of_all_row + 1) / len(list_row_in_col)
            all_counter_list.append((column, avg_len, counter_list))
        is_test = False
        if is_test:
            for x in all_counter_list:
                print("powiinno", x[0], end=" | ")
                print(self.most_probably(x))
        return all_counter_list

    "tu na pewno pasuje zrobić coś lepszego ale niech na razie bedzie"
    "potem na pewno lepiej żeby przyjmował wszystkie kolumny i rozdzieał nazwy po tym która najbardziej pasuje do której"

    def most_probably(self, counter_list):
        if counter_list[1] > 4:
            return self.names_list[3]
        else:
            counter_list[2][3] = 0
        arg_max = np.argmax(counter_list[-1])
        if counter_list[-1][arg_max] == 0:
            return "empty"
        return self.names_list[arg_max]

    "tu pasowało by dodać wiecej słów i może je też jakoś ujednolicić np przerabiać zawsze tabl. na tabletka przed wgraniem do słownika jak i przed użyciem go " \
    "przy klasyfikacji"

    def make_dictionary(self, data_frame):
        how_many_word = 4
        expected_name = expected_name_1
        for name in expected_name:
            standard = self.make_standard_string(name)
            self.dict_of_set[standard] = set({})
            self.names_list.append(standard)
        for column in data_frame:
            list_row_in_col = data_frame[column]
            for row in list_row_in_col:
                standard = self.make_standard_string(row)
                words_in_row = standard.split()[:how_many_word]
                for word in words_in_row:
                    standard_word = self.make_standard_string(word)
                    standard_column = self.make_standard_string(column)
                    if standard_word != "nan":
                        self.dict_of_set[standard_column].add(standard_word)

# column_classifier = ColumnClassifier()
