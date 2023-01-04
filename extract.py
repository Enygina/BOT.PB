# функция принимает на вход список списков, осуществляет поиск значения, возвращаент новый список найденных совпадений
def fnd_lastname(data, search):
    fnd_res = []
    s = [item for sublist in search for item in sublist]
    for i in range(len(data)):
        if s[0] == data[i][0]:
            fnd_res.append(data[i])
    return fnd_res


# функция проверяет список на пустоту
def empty_fnd(data):
        if not data:
            return -1
        else:
            return data
