from datetime import datetime as dt


def log_data(data):
    time = dt.now().strftime('%d.%m.%y %H:%M')
    with open('log.csv', 'a') as f:
        f.write('{}; {}\n'.format(time, data))

