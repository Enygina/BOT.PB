## Telegram bot телефонная книга 

Бот предназначен для:
1. Получения и хранения данных :
- фамилия
- имя
- телефон
- описание
2. Вывода фото дня и  информации о нет с сайта NASA
3. Для вывода данных прогноза погоды по названию города

# Модули программы

**main**
Модуль, запускающий выполнение программы.
___________________
**app**

Инициализация бота.

___________________

**config**

Хранит token бота, 
Chat id

___________________
**handlers**

Модуль содержит все команды для бота, классы состояний.

___________________
**keyboards**

Содержит функцию для создания клавиатур.

___________________
**Logger**  

Модуль, осущестялющий логирование операций и запись истории операций в файл log.scv. Запись осуществлется в следующем формате:
- Дата и время совершения операции, 
- введенные данные

***Файл log.csv*** предназначен для хранения записей об истории занесения данных.
___________________

**Extract**   

Модуль поиска по фамилии
___________________

**Recording_data** 

Модуль осуществляет запись в csv файлы и вывод данных из этих файлов, открытие фото

файлы с данными:
- ***Файл for_find.csv***
- ***Файл log.csv***
- ***Файл Names.csv***
- ***Файлы .jpg***
___________________

