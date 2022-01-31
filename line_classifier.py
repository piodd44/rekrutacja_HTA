import math
import numpy as np

nan = "nan"
list_start_0 = []
list_start_1 = []
list_is_1 = ["lp", "lp.", "l.p."]
list_start_1.append("lp")
list_start_1.append("lp.")
list_start_1.append("l.p.")
#list_start_1.append("nazwa")
#list_start_1.append("ilość")
#list_start_1.append("cena")
#list_start_1.append("wartość")
#list_start_1.append("opis")
#list_start_1.append("jednostka")
list_start_2 = []
list_start_2.append("zadanie")
list_start_2.append("pakiet")
list_number = [str(x) for x in range(0, 15)]
"można by tu dodać coś bardziej zawansowanego jak by był wieksza baza nawet zliczanie pewnych słow kluczowych i potem jakiś uczene maszynowe na tym "


class LineClassifier:
    def __init__(self):
        self.possible_start_set_0 = set({})
        self.possible_start_set_1 = set({})
        self.possible_start_set_2 = set({})
        self.is_one_set = set({})
        self.number_set = set({})
        self.__create_sets__()

    def __create_sets__(self):
        for x in list_start_0:
            self.possible_start_set_0.add(x)
        for x in list_start_1:
            self.possible_start_set_1.add(x)
        for x in list_start_2:
            self.possible_start_set_2.add(x)
        for x in list_number:
            "na razie uznaje ze same cyfry to pewnie start bo to sa numery koloumn"
            self.possible_start_set_1.add(x)
        for x in list_is_1:
            self.is_one_set.add(x)

    def get_row_class(self, row):
        length_row = len(row)
        "numerki oznaczaja o ile w du prawdopodobnie trzeba przejść by już mieć dane a nie np opis kolumn"
        nr_of_nan = 0
        nr_of_start_0 = 0
        nr_of_start_1 = 0
        nr_of_start_2 = 0
        nr_of_non_recognize = 0
        "to potem do poprawy bo brzydkie "
        #print(row[0])
        for y in row:
            try:
                z = str(y).rstrip("\n")
                split_str = str(z).lower().split()
                for some_str in split_str:
                    y = some_str.strip()
                    if y != "":
                        break
                x = y
            except:
                print("w except")
                break
            if x == nan:
                nr_of_nan += 1
            elif x in self.is_one_set:
                #print("pewniak")
                return "start_1"
            elif x in self.possible_start_set_0:
                nr_of_start_0 += 1
            elif x in self.possible_start_set_1:
                nr_of_start_1 += 1
            elif x in self.possible_start_set_2:
                nr_of_start_2 += 1

            else:
                nr_of_non_recognize += 1
                # print(type(x), "|", x)

        proportion_start_0 = nr_of_start_0 / length_row
        proportion_start_1 = nr_of_start_1 / length_row
        proportion_start_2 = nr_of_start_2 / length_row
        proportion_of_nan = nr_of_nan / length_row
        proportion_of_non_recognize = nr_of_non_recognize / length_row
        proportion_list = [proportion_start_0, proportion_start_1, proportion_start_2, proportion_of_non_recognize]
        names_of_class = ["start_0", "start_1", "start_2", "non-recognize"]
        my_max = np.argmax(proportion_list)
        show = False
        if show:
            print(row)
            print("nr_of_nan==", nr_of_nan)
            print("nr_of_start_0==", nr_of_start_0)
            print("nr_of_start_1==", nr_of_start_1)
            print("nr_of_start_2==", nr_of_start_2)
            print("nr_of_non_recognize", nr_of_non_recognize)
            print("proportion_start_0==", proportion_start_0)
            print("proportion_start_1==", proportion_start_1)
            print("proportion_start_2==", proportion_start_2)
            print("proportion_of_nan==", proportion_of_nan)
        if nr_of_nan == length_row:
            #print("empty")
            return "empty"
        else:
            #print(names_of_class[my_max])
            return names_of_class[my_max]
