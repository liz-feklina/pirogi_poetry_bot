# @pirogi_poetry_bot

![пример использования](https://github.com/liz-feklina/pirogi_poetry_bot/blob/main/Снимок%20экрана%202025-05-16%20233330.png?raw=true)

## Содержание репозитория:
- aot_crawler + pirozhki - тетрадка с кодом
- codenames_biggest_one - изначальный набор слов
- codenames_big_dicts.pickle - готовые словари
- bot.py - код телеграм-бота

## Описание проекта

### Пирожки

Данная программа генерирует пирожки

Что такое пирожки? Это современный жанр поэзии, о его структуре можно почитать в [Википедии](https://ru.wikipedia.org/wiki/%D0%9F%D0%B8%D1%80%D0%BE%D0%B6%D0%BE%D0%BA_(%D0%BF%D0%BE%D1%8D%D0%B7%D0%B8%D1%8F)), популярные примеры можно посмотреть [вот здесь](https://poetory.ru/pir/likes).

У пирожков есть несколько больших преимуществ для генерации:
- нет рифмы (нужно разбираться только с ритмом)
- чётко заданный размер строки и слог
- всё пишется с маленькой буквы и без знаков препинания
- шутливость, иногда доходящая до абсурда (странные результаты программы выглядят не так уж и плохо для любителей такого жанра)



### Опрашивание сайта и хранение результатов

Для того, чтобы получить данные об ударении, был использован http://aot.ru/demo/morph.html и хитрый способ подавать запрос :)
В качестве словаря были использованы слова с https://codenames.me.  На нём представлены только существительные, но после разных попыток стало понятно, что на данном уровне стихотворения только из существительных выглядят интереснее, тогда как если добавить глаголы, появляется много форм (все формы, в т.ч. причастий во всех родах), и словарь замусоривается.

Для каждого существительного была взята полная парадигма, если было несколько вариантов ударения, брались оба (хотя некоторые из них очень странные, автоматически определять адекватность данных, конечно, невозможно)

Для хранения данных был выбран способ создать два словаря, в одном из которых ключами являются пара количество слогов+номер ударного, а значением множество с подходящими словами, а второй наоборот, хранит для каждого слова информацию о количестве слогов и номере ударного слога в нём.

Для хранения созданного словаря был выбран формат pickle, так как в json-словаре ключ не может быть кортежем.



### Дополнительные штуки

Помимо обычной генерации, в результате которой получается ритмически подходящие слова, которые однако не соединяются ни во что связное, были добавлены "шаблоны", в которых есть вспомогательные строки и закреплен падеж, в результате чего пирожок всё ещё порождён программой, но обретает какой-то смысл, и их уже становится интереснее читать. Кажется, с помощью этого метода можно получить действительно интересный и достаточно оригинальный результат.

Кроме того, была добавлена семантическая модель: по заданному слову создаётся его личный словарь (у сайта опрашивают данные об ударении в 200 близких словах), который можно использовать в обычной генерации и шаблонах. Иногда получается очень красиво :)


### Телеграм-бот

http://lizfeklina.pythonanywhere.com/

В телеграм-боте (который можно найти по названию, указанному в заголовке) присутствуют все возможности, кроме семантического анализа. Семантическая модель занимает довольно много места + создание индивидуального словаря работает медленно, что не очень подходит для бота.
