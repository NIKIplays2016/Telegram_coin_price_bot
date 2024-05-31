import telebot
import json

token=''
bot=telebot.TeleBot(token)

def update_date():
    with open(r"base\userbase.json", "r", encoding="utf-8") as file:
        mdir = json.load(file)
    return mdir

def save(mdir):
    with open(r"base\userbase.json", "w", encoding="utf-8") as file:
        json.dump(mdir, file, ensure_ascii=False)

def bot_write(id, sms):
    global bot
    try:
        bot.send_message(id,sms)
    except:
        print(f"bot was blocked by the {id}")



#############################################

def registrate(message, base):
    id = message.chat.id
    base["id"].append(id)
    base["root"].append(False)
    base["none_reg"].remove(id)
    base["bool_actions"].append([False, False, False, False, False, False, False])
    base["spam"]["token"].append([])
    base["warning"]["token"].append([])
    base["warning"]["limit"].append([])
    if id > 0:
        base["name"].append(message.from_user.user_name)
    elif id < 0:
        base["name"].append(message.chat.title)
    save(base)

    bot.reply_to(message, text="Successful registration")



def bot_main():
    with open("base\static.json", "r") as file:
        token_base = json.load(file)


    global bot

    def check_registrate(id, base) -> bool:
        if id in base["id"]:
            return True
        else:
            return False

    def check_admin(message, base) -> bool:

        try:
            chat_index = base["id"].index(message.chat.id)
        except:
            return False

        try:
            user_index = base["id"].index(message.from_user.id)
        except:
            return False

        if base["root"][chat_index] or base["root"][user_index]:
            return True
        else:
            return False


    def reset_actions():
        return [False, False, False, False, False, False, False]

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        id = message.chat.id
        base = update_date()
        if id not in base["id"] and not id in base["none_reg"]:
            bot.reply_to(message, text="Введите пароль")
            base["none_reg"].append(id)
            save(base)



    @bot.message_handler(commands=['command1'])
    def handle_start(message):
        id = message.chat.id
        base = update_date()
        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0
        index = base["id"].index(id)

        if id in base["black_list"]:
            bot.reply_to(message, f"Вы были заблокированы. \nПоддержка: @picard_off")
            return 0

        base["bool_actions"][index] = reset_actions()

        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        for i in token_base["tokens"]:
            keyboard1.row(i)

        base["bool_actions"][index][6] = True
        bot.reply_to(message, "Введите короткое название монеты", reply_markup=keyboard1)
        save(base)

    @bot.message_handler(commands=['command2'])
    def handle_start(message):
        id = message.chat.id
        base = update_date()
        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0
        index = base["id"].index(id)

        if id in base["black_list"]:
            bot.reply_to(message, f"Вы были заблокированы. \nПоддержка: @picard_off")
            return 0

        base["bool_actions"][index] = reset_actions()

        base["bool_actions"][index][0] = True
        bot.reply_to(message, "Введите через пробел короткое называние монеты и пределы. \n\nПример: \TON 6.43 7.1")

        save(base)

    @bot.message_handler(commands=['command3'])  # Удаление монеты из warning
    def handle_start(message):
        id = message.chat.id
        base = update_date()
        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0
        index = base["id"].index(id)

        if id in base["black_list"]:
            bot.reply_to(message, f"Вы были заблокированы. \nПоддержка: @picard_off")
            return 0

        base["bool_actions"][index] = reset_actions()

        base["bool_actions"][index][5] = True
        bot.reply_to(message, "Введите короткое название монеты")

        save(base)









    @bot.message_handler(commands=['about_me'])
    def handle_start(message):
        id = message.chat.id
        base = update_date()
        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0
        index = base["id"].index(id)

        if id in base["black_list"]:
            bot.reply_to(message, f"Вы были заблокированы. \nПоддержка: @picard_off")
            return 0

        sms = f"id: {id}"

        sms += "\n\nУведомления о цене:"
        sms += f"\n{base['spam']['token'][index]}"

        sms += "\n\nУведомления при выходе монеты из ценового диапазона:\n"
        for i in range(len(base['warning']['token'][index])):
            sms += f"\nМонета: {base['warning']['token'][index][i]} \nЦеновой диапазон: с {base['warning']['limit'][index][i][0]} до {base['warning']['limit'][index][i][1]}\n"

        bot.reply_to(message, sms)



###########################################################s
    """определить и вызвать функцию, понимать механизм перегрузки"""



    @bot.message_handler(commands=['command0', "help", "info"])
    def handle_start(message):
        bot.reply_to(
            message,
            text=f""" 
'Coin price' - Это Telegram бот позволяющий следить за ценой разных криптовалют.
v0.50 Beta

Информация о цене берется с okx.com

Команды:
 /command1 - При вводе этой команды бот будет присылать каждую минуту цену на введенную вами монету, чтобы отписаться нужно повторно ввести команду.

 /command2 - При вводе этой команды бот предлагает вам ввести название монеты, верхний и нижний "предел" цены. 
При переходе нижнего или верхнего предела цены, бот уведомит вас об этом. 

 /command3 - При вводе этой комманды нужно ввести название монеты, и вам больше не будут приходить уведомления о выходе цены этой манеты из ценового диапазона который вы указали ранее (/command2)  


@picard_off
19.05.2024
okx API 
               """
        )

    @bot.message_handler(commands=['id_list'])
    def handle_start(message):
        base = update_date()

        if not check_admin(message, base):
            bot.reply_to(message, "У вас нет прав для этой команды")
            return 0

        indexes = base["id"]
        names = base["name"]

        sms = ""
        for i in range(len(indexes)):
            sms += f"\n {i}: {names[i]} - {indexes[i]}"

        bot.reply_to(message, sms)

    @bot.message_handler(commands=['admin'])
    def handle_start(message):
        base = update_date()

        if not check_admin(message, base):
            bot.reply_to(message, "У вас нет прав для этой команды")
            return 0

        bot.reply_to(message, "Команды Администратора: \n/id_list \n/ban \n/black_list \n\nКоманды главного Администратора: \n/add_admin \n/delete_admin \n/change_main_admin ")


    @bot.message_handler(commands=["add_admin"])
    def handle_start(message):
        id = message.chat.id
        base = update_date()

        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0

        index = base["id"].index(id)
        if not id == base["main_admin"]:
            bot.reply_to(message, "У вас нет прав для этой команды. Это может делать только главный админ")
            return 0

        base["bool_actions"][index] = reset_actions()

        base["bool_actions"][index][2] = True
        bot.reply_to(message, "Введите id пользователя")
        save(base)

    @bot.message_handler(commands=["delete_admin"])
    def handle_start(message):
        id = message.chat.id
        base = update_date()

        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0

        index = base["id"].index(id)
        if not id == base["main_admin"]:
            bot.reply_to(message, "У вас нет прав для этой команды. Это может делать только главный админ")
            return 0

        base["bool_actions"][index] = reset_actions()

        base["bool_actions"][index][3] = True
        bot.reply_to(message, "Введите id пользователя")
        save(base)

    @bot.message_handler(commands=["change_main_admin"])
    def handle_start(message):
        id = message.chat.id
        base = update_date()

        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0

        index = base["id"].index(id)
        if not id == base["main_admin"]:
            bot.reply_to(message, "У вас нет прав для этой команды. Это может делать только главный админ")
            return 0

        base["bool_actions"][index] = reset_actions()

        base["bool_actions"][index][4] = True
        bot.reply_to(message, "Введите id пользователя")
        save(base)

    @bot.message_handler(commands=['ban'])
    def handle_start(message):
        id = message.chat.id
        base = update_date()

        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0

        index = base["id"].index(id)

        if not check_admin(message, base):
            bot.reply_to(message, "У вас нет прав для этой команды")
            return 0

        base["bool_actions"][index] = reset_actions()

        base["bool_actions"][index][1] =True
        bot.reply_to(message, "Введите id и действие(0 - убрать из чс, 1 - добавить в чс) \n\nПример: \n1913991 1")
        save(base)



    @bot.message_handler(commands=['black_list'])
    def handle_start(message):
        id = message.chat.id
        base = update_date()

        if not check_registrate(id, base):
            bot.reply_to(message, text="Вы не авторизованны. \nВведите пароль")
            return 0

        if not check_admin(message, base):
            bot.reply_to(message, "У вас нет прав для этой команды")
            return 0

        ids = base["id"]
        names = base["name"]
        black_list = base["black_list"]
        if len(black_list) == 0:
            bot.reply_to(message, "Черный список пуст")
        else:
            sms = ""
            for i in range(len(black_list)):
                try:
                    index = ids.index(black_list[i])
                    sms += f"\n {i}: {names[index]} - {black_list[i]}"
                except:
                    sms += f"\n {i}: Noname - {black_list[i]}"
            bot.reply_to(message, sms)





    @bot.message_handler(content_types=['text', 'document', 'audio', 'photo', 'video'])
    def get_text_messages(message):
        base = update_date()
        id = message.chat.id
        print(message)

        admin = check_admin(message, base)


        if id in base["black_list"] and id > 0 and not admin:
            bot.reply_to(message, f"Вы были заблокированы.😬 \nПоддержка: @picard_off")
            return 0
        elif id in base["black_list"] and id < 0 and not admin:
            bot.reply_to(message, f"Группа была заблокирована.😬 \nПоддержка: @picard_off")
            return 0


        if id not in base["id"] and not id in base["none_reg"]:
            bot.reply_to(message, text="Введите пароль")
            base["none_reg"].append(id)
            save(base)
            return 0

        elif id in base["none_reg"]:
            if message.text == "10701323":
                registrate(message, base)
            else:
                bot.reply_to(message, text="Не верный пароль")
                bot.send_message(id, "Введите пароль заново")
            return 0

        else:
            index = base["id"].index(id)



        if base["bool_actions"][index][0]:
            try:
                command = message.text.split(" ")
                token, command[1], command[2] = command[0].upper(), float(command[1]), float(command[2])
            except:
                bot.reply_to(message, "❌Неверный ввод❌ \nПопробуйте заново нажав на команду /command2")
                base["bool_actions"][index][0] = False
                return 0

            if not token in token_base["tokens"]:
                bot.reply_to(message, "Такой монеты к нет в списке")
                base["bool_actions"][index][0] = False
                return 0

            """if token in base["warning"]["token"][index]:
                token_index = base["warning"]["token"][index].index(token)
                base["warning"]["token"][index].remove(token)
                base["warning"]["limit"][index].pop(token_index)
                bot.reply_to(message, f"Теперь вам не будет приходить уведомление о {token}")"""

            if token in base["warning"]["token"][index]:
                token_index = base["warning"]["token"][index].index(token)
                base["warning"]["limit"][index][token_index] = [command[1], command[2]]
                bot.reply_to(message, f"Теперь вам будет приходить уведомление когда цена {token} \nПовысится до {command[2]}$ \nУпадет до {command[1]}$")
            else:
                base["warning"]["token"][index].append(token)
                base["warning"]["limit"][index].append([command[1], command[2]])
                bot.reply_to(message, f"Теперь вам будет приходить уведомление когда цена {token} \nПовысится до {command[2]}$ \nУпадет до {command[1]}$")

            base["bool_actions"][index][0] = False
            save(base)


        elif base["bool_actions"][index][1]:
            command = message.text.split(" ")
            try:
                command[0], command[1] = int(command[0]), int(command[1])
            except:
                bot.reply_to(message, "Ошибка ввода")
                base["bool_actions"][index][1] = False
                save(base)
                return 0

            try:
                if command[1] == 0:
                    base["black_list"].remove(command[0])
                    bot.reply_to(message, f"Пользователь {command[0]} теперь не в черном списке")
                elif command[1] == 1:
                    if not command[0] in base["black_list"]:
                        base["black_list"].append(command[0])
                        bot.reply_to(message, f"Пользователь {command[0]} теперь в черном списке")
                    else:
                        bot.reply_to(message, "Пользователь уже находиться в черном списке")
            except:
                bot.reply_to(message, "Этого пользователя нет в черном списке")

            base["bool_actions"][index][1] = False
            save(base)

        elif base["bool_actions"][index][2]:
            try:
                nid = int(message.text)
            except:
                bot.reply_to(message, "Неверный ввод")
                base["bool_actions"][index][2] = False
                return 0

            try:
                nindex = base["id"].index(nid)
                base["root"][nindex] = True
                bot.reply_to(message, f"Пользователь {nid} теперь администратор")
            except:
                bot.reply_to(message, f"Пользователь {nid} не найден")
            base["bool_actions"][index][2] = False
            save(base)


        elif base["bool_actions"][index][3]:
            try:
                nid = int(message.text)
            except:
                bot.reply_to(message, "Неверный ввод")
                base["bool_actions"][index][3] = False
                save(base)
                return 0

            try:
                nindex = base["id"].index(nid)
                base["root"][nindex] = False
                base["bool_actions"][index][3] = False
                bot.reply_to(message, f"Пользователь {nid} теперь не администратор")

            except:
                bot.reply_to(message, f"Пользователь {nid} не найден")
            base["bool_actions"][index][3] = False
            save(base)

        elif base["bool_actions"][index][4]:
            try:
                nid = int(message.text)
            except:
                bot.reply_to(message, "Неверный ввод")
                base["bool_actions"][index][4] = False
                save(base)
                return 0

            bot.reply_to(message, f"Главный админ изменен с {base['main_admin']} на {nid}")
            base["main_admin"] = nid
            base["bool_actions"][index][4] = False
            save(base)





        elif base["bool_actions"][index][5]: #Удаление токена с warning
            token = message.text.upper()


            if token in base["warning"]["token"][index]:
                token_index = base["warning"]["token"][index].index(token)
                base["warning"]["token"][index].remove(token)
                base["warning"]["limit"][index].pop(token_index)
                bot.reply_to(message, f"Теперь вам не будет приходить уведомление о {token}")
            else:
                bot.reply_to(message, f"У вас не стоит 'колокольчик' на {token}")
            base["bool_actions"][index][5] = False

            save(base)

        elif base["bool_actions"][index][6]:
            sms = message.text.upper()
            if not sms in token_base["tokens"]:
                bot.reply_to(message, "Такой монеты к нет в списке")
                base["bool_actions"][index][6] = False
                return 0

            if sms in base["spam"]["token"][index]:
                base["spam"]["token"][index].remove(sms)
                bot.reply_to(message, f"Теперь вы не будете получать рассылку цены на {sms}")
            else:
                base["spam"]["token"][index].append(sms)
                bot.reply_to(message, f"Теперь вы будете получать рассылку цены на {sms}")
            base["bool_actions"][index][6] = False
            save(base)


    bot.polling(none_stop=True, interval=0)
