import csv


def rec_csv(data, f_n):
    with open('Names.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=f_n, extrasaction='ignore')
        writer.writeheader()
        writer.writerow(data)


def for_fnd(data, f_n):
    with open('for_find.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=f_n, extrasaction='ignore')
        writer.writeheader()
        writer.writerow(data)


def output_csv(a):
    with open(a) as f:
        reader = csv.reader(f)
        return list(reader)


def for_beauty(a):
    j = [x for x in a if x != []]
    for i in j:
        if i[0] != 'Surname':
            j.remove(i)
    return j
