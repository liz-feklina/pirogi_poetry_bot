import telebot
import conf
#import pickle
import pickle5 as pickle
import random
import flask

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

with open('codenames_big_dicts.pickle', 'rb') as handle:
    original_dict_list = pickle.load(handle)
accent_dict, word_dict, nom_accent_dict, nom_word_dict, ins_accent_dict, ins_word_dict, dat_accent_dict, dat_word_dict, acc_accent_dict, acc_word_dict = original_dict_list


def poetry(n, ac, dict_accents, dict_words):
    stroka = []
    str_len = ac  # (уже заполнено)
    full = n + ac  # (длина итоговой строки)

    while True:
        if full - str_len == 3:
            word = random.choice(list(dict_accents[(3, str_len % 2 + 2)]))
            stroka.append(word.lower())
            str_len += 3
            break
        if full - str_len == 1:
            word = random.choice(list(dict_accents[(1, 1)]))
            stroka.append(word.lower())
            str_len += 1
            break
        else:
            # keys = (любое число от 1 до 4, набор ударений: или [1,3] или [2,4]str_len%2)
            keys = []
            if str_len % 2 == 0:
                accents = [2, 4]
            else:
                accents = [1, 3]
            for i in range(1, min(4, full - str_len + 1)):
                if (full - str_len - i) != 1:
                    for j in accents:
                        if not (full - str_len == 4 and i == 4 and j in [1, 2]):
                            keys.append((i, j))
            w_list = []
            for key in keys:
                w_list.extend(list(dict_accents[key]))
            word = random.choice(w_list)
            stroka.append(word.lower())
            str_len += list(dict_words[word])[0][0]
            if full - str_len == 1:
                print(stroka)
        if str_len == full:
            break
    return ' '.join(stroka)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, эта программа генерирует пирожки!\n/random - пирожок генерируется с нуля\n/template1, /template2, /template3, /template4 - пирожок с вспомогательными строками и структурой\n\n(Чтобы получить вот эту инструкцию, тыкните /start или /help)")


@bot.message_handler(commands=['random'])
def random_poem(message):
    poem = poetry(9, 2, accent_dict, word_dict) + '\n' + poetry(8, 2, accent_dict, word_dict) + '\n' + poetry(9, 2, accent_dict, word_dict) + '\n' + poetry(8, 2, accent_dict, word_dict)
    bot.send_message(message.chat.id, poem)


@bot.message_handler(commands=['template1'])
def template1(message):
    poem = 'заходит в дом олег под вечер\nа там ' + poetry(6, 2, nom_accent_dict, nom_word_dict) + '\n' + poetry(9, 2, nom_accent_dict, nom_word_dict) + '\nи дом вообще-то не его'
    bot.send_message(message.chat.id, poem)


@bot.message_handler(commands=['template2'])
def template2(message):
    poem = 'оксана мчится ' + poetry(4, 1, ins_accent_dict, ins_word_dict) + '\n' + poetry(8, 2, ins_accent_dict, ins_word_dict) + '\n' + poetry(9, 2, ins_accent_dict, ins_word_dict) + '\nно магазин уже закрыт'
    bot.send_message(message.chat.id, poem)


@bot.message_handler(commands=['template3'])
def template3(message):
    poem = 'у роботов другие чувства\nне ' + poetry(1, 1, nom_accent_dict, nom_word_dict) + ' не ' + poetry(2, 1, nom_accent_dict, nom_word_dict) + ' не ' + poetry(2, 2, nom_accent_dict, nom_word_dict) + '\nа ' + poetry(8, 1, nom_accent_dict, nom_word_dict) + '\n' + poetry(5, 2, nom_accent_dict, nom_word_dict) + ' и ' + poetry(2, 2, nom_accent_dict, nom_word_dict)
    bot.send_message(message.chat.id, poem)


@bot.message_handler(commands=['template4'])
def template4(message):
    poem = '\n'.join([random.choice(list(dat_accent_dict[(3, 2)])).lower() + ' ' +
                      random.choice(list(acc_accent_dict[(3, 1)])).lower() + ' и ' +
                      random.choice(list(acc_accent_dict[(2, 1)])).lower(),
                      random.choice(list(dat_accent_dict[(2, 2)])).lower() + ' ' +
                      random.choice(list(acc_accent_dict[(4, 2)])).lower() + ' и ' +
                      random.choice(list(acc_accent_dict[(1, 1)])).lower(),
                      random.choice(list(dat_accent_dict[(3, 2)])).lower() + ' ' +
                      random.choice(list(acc_accent_dict[(1, 1)])).lower() + ' и ' +
                      random.choice(list(acc_accent_dict[(4, 3)])).lower(),
                      'а мне ' + random.choice(list(acc_accent_dict[(3, 2)])).lower() +
                      ' и ' + random.choice(list(acc_accent_dict[(2, 2)])).lower()])
    bot.send_message(message.chat.id, poem)


@bot.message_handler(content_types=["text"])
def text(message):
    bot.send_message(message.chat.id, "Я не очень разговорчивый...")



# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
