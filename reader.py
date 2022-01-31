import pandas as pd
from line_classifier import LineClassifier
from column_classifier import ColumnClassifier


def open_xlms(path):
    xl = pd.ExcelFile(path)
    res = len(xl.sheet_names)
    data_frame = pd.read_excel(path)
    return data_frame


def pure_data_frame(path, start_sheet=0):
    print("w funkcji")
    xl = pd.ExcelFile(path)
    res = len(xl.sheet_names)
    counter = 0
    error_list = []
    line_classifier = LineClassifier()
    all_data_frame_list = []
    headers = ["non_start"]
    for name_of_sheet in xl.sheet_names:
        counter += 1
        # to dla testwów żeby nie czekać zbyt długo na wynik
        if counter > 30:
            break
        # tu wcześniej można bywykryć od kiedy zacząć , na razie na sztywno
        if counter > start_sheet:
            print("cunter==", counter, name_of_sheet)
            data_frame = pd.read_excel(path, sheet_name=name_of_sheet)
            data_frame = data_frame.dropna(how="all", axis=1)
            start_end_index = find_start_end_table_index(data_frame=data_frame, line_classifier=line_classifier)
            good_row_list = []
            for start, end in start_end_index:
                [good_row_list.append(x) for x in range(start, end)]

            # to na pewno trzeba lepiej robić
            if headers[0] == "non_start":
                headers_index = start_end_index[0][0] - 1
                headers = data_frame[data_frame.index.isin([headers_index])].values[0]
            data_frame.columns = headers
            data_frame = data_frame[data_frame.index.isin(good_row_list)]
            data_frame["pakiet"] = name_of_sheet
            data_frame = data_frame.reset_index(drop=True)
            all_data_frame_list.append(data_frame)
    print("llen all data frame list", len(all_data_frame_list))
    if len(all_data_frame_list) > 1:
        data_frame = pd.concat(all_data_frame_list)
    # data_frame.to_csv('test_1_all_nowe.csv')
    # print(data_frame)
    print("zwacamy")
    return data_frame


"plan taki ze wybieramy possible start ten dalszy o jeden jeśli jest"


def find_start_end_table_index(data_frame, line_classifier):
    # data_frame = data_frame.head()
    # to pewnie troche wolne ale na razie niech bedzie
    possible_start_0 = []
    possible_start_1 = []
    possible_start_2 = []
    possible_start_list = []
    row_class_list = []
    for index_r, row in data_frame.iterrows():
        # print("========== wiersz  start =========")
        row_list = list(row)
        # print(index_r, row_list)
        possible_class = line_classifier.get_row_class(row_list)
        # print("row list==",row_list)
        if possible_class == "start_2":
            possible_start_2.append((index_r, row_list))
            possible_start_list.append((index_r, 2))
        if possible_class == "start_1":
            possible_start_list.append((index_r, 1))
            possible_start_1.append((index_r, row_list))
        if possible_class == "start_0":
            possible_start_list.append((index_r, 0))
            possible_start_0.append((index_r, row_list))
        row_class_list.append((index_r, possible_class, row_list))
    for x in row_class_list:
        # print(x)
        pass
    close_index_pack = []
    start_table_index_list = []
    pos_len = len(possible_start_list)
    last_index = possible_start_list[0][0] - 1
    for row_index, row_class in possible_start_list:
        pos_len -= 1
        # print(last_index, row_index)
        if row_index - last_index == 1:
            close_index_pack.append((row_index, row_class))
        else:
            start_table_index_list.append(close_index_choose(close_index_pack))
            close_index_pack = []
            close_index_pack.append((row_index, row_class))
        if pos_len == 0:
            start_table_index_list.append(close_index_choose(close_index_pack))
            close_index_pack = []
            close_index_pack.append((row_index, row_class))
        last_index = row_index
    start_end_index_list = []
    for start_index in start_table_index_list:
        start_end_index_list.append(
            (start_index, find_end_of_table(start_index=start_index, row_class_list=row_class_list)))
    # for x in start_end_index_list:
    # print(x)
    return start_end_index_list


"konców bedziemy szukać idąc od spodziewanych początków do np nan albo czegoś co już nie jest liczbą (jesli sa numerowane ) "


def close_index_choose(pack):
    # print(pack)
    return pack[-1][0] + pack[-1][1]


number_list = [str(x) for x in range(10)]


def find_end_of_table(start_index, row_class_list):
    cur_index = start_index
    "tu wiadomo ze pasowało by rozbudować"
    while True:
        index_r, class_r, line = row_class_list[cur_index]
        if type(line[0]) is int:
            pass
        elif str(line[0])[0] in number_list:
            pass
        else:
            # print("end ", row_class_list[cur_index])
            # print("before end", row_class_list[cur_index - 1])
            return cur_index
        cur_index += 1


def make_good_columns(data_frame):
    column_classifier = ColumnClassifier(open_xlms("output.xlsx"))
    canter_list = column_classifier.counter_for_columns(data_frame)
    all_class_name = []
    for x in canter_list:
        class_col = column_classifier.most_probably(counter_list=x)
        all_class_name.append(class_col)
    data_frame.columns = all_class_name
    data_frame = data_frame.drop(['empty'], axis=1)
    return data_frame


def test_1():
    path = "zad4.xlsx"
    df = pure_data_frame(path)
    print(df)
    column_classifier = ColumnClassifier(open_xlms("output.xlsx"))
    print("====================")
    canter_list = column_classifier.counter_for_columns(df)
    for x in canter_list:
        class_col = column_classifier.most_probably(counter_list=x)
        print(class_col)


def test_2():
    path = "test_1.xlsx"
    pure_data_frame(path, start_sheet=1)

def test_3():
    path = "zad4.xlsx"
    df = pure_data_frame(path)
    df_good = make_good_columns(df)
    df_good.to_csv('test_4_all_nowe_col.csv')


def test_4():
    path = "test_1.xlsx"
    df = pure_data_frame(path, start_sheet=1)
    df_good = make_good_columns(df)
    df_good.to_csv('test_1_all_nowe_col.csv')


# test_1()
# column_classifier = ColumnClassifier(open_xlms("output.xlsx"))
test_3()
test_4()
