names_list = []
opakowanie = ["opakowanie", "op", "op."]
names_list.append(opakowanie)
fiolka = ["fiolka", "fiol", "fiol."]
names_list.append(fiolka)
ampulka = ["ampułka", "amp", "amp."]
names_list.append(ampulka)
tubka = ["tubka", "tb"]
names_list.append(tubka)
tabletka = ["tabletka", "tabl", "tabl."]
names_list.append(tabletka)
szaszetka = ["saszetka", "sasz", "sasz."]
names_list.append(szaszetka)
butelka = ["butelka", "but.", "but"]
names_list.append(butelka)
sztuka = ["sztuka", "szt.", "szt"]
names_list.append(sztuka)
miss = ["miss", "nan"]
names_list.append(miss)
worek = ["worek"]
names_list.append(worek)
flakon = ["flakon", "flak."]
names_list.append(flakon)
plaster = ["plaster"]
names_list.append(plaster)
kapsulka = ["kasułka", "kaps."]
names_list.append(kapsulka)
wstrzykiwacz = ["wstrzykiwacz"]
names_list.append(wstrzykiwacz)
strzykawka = ["strzykawka", "strz."]
names_list.append(strzykawka)
wklad = ["wkład", "wkł."]
names_list.append(wklad)
wlewka = ["wlewka"]
names_list.append(wlewka)
gram = ["gram"]
names_list.append(gram)
czopek = ["czopek", "czop."]
names_list.append(czopek)
drazetka = ["drażetka", "draż."]
names_list.append(drazetka)


class DictionaryMED():
    def __init__(self):
        self.package_med = {}
        self.create_package_med()
        self.not_in_package_med = set({})

    def create_package_med(self):
        for synonyms_list in names_list:
            for name in synonyms_list:
                self.package_med[name] = synonyms_list[0]
        test = True

    # potem jakieś błedy dopisać
    # potem zrobić na regex na np amp.-strz.
    def give_one_name(self, synonym):
        if type(synonym) == str:
            synonym = synonym.lower()
            synonym = synonym.strip()
        standard_name = self.package_med.get(synonym)
        if standard_name is not None:
            return standard_name
        else:
            # potem to gdzieś zapisywać
            self.not_in_package_med.add(synonym)
            return synonym


def test_dict():
    print("========= test_dict ============")
    dict_med = DictionaryMED()
    expected_opakowanie = "opakowanie"
    opakowanie = [dict_med.give_one_name("op"), dict_med.give_one_name("op."),
                  dict_med.give_one_name("opakowanie")]
    for x in opakowanie:
        print(x == expected_opakowanie)
    print("========= end test_dict ==========")
    print(dict_med.give_one_name("opasdas"))


test_dict()
