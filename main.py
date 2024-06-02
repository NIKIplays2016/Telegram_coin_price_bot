from modules.tg_bot import *
from modules.spot_price import *

import json

from threading import Thread
from time import sleep




def check_price():
    with open("base\static.json", "r") as file:
        token_base = json.load(file)

    tick = 0

    while True:
        base = update_date()
        while True:
            price = get_price(token_base)
            keys_list = list(price.keys())

            if len(keys_list) == len(token_base["tokens"]):
                break


        print(price)

        for a in range(len(base["warning"]["token"])):
            user_id = base["id"][a]
            if not user_id in base["black_list"]:
                for b in range(len(base["warning"]["token"][a])):
                    local_token = base["warning"]["token"][a][b]
                    try:
                        local_price = float(price[local_token])

                        if local_price > base["warning"]["limit"][a][b][1]:
                            bot_write(
                                user_id,
                                f"❕💸💸💸 \nЦена {local_token}:{local_price} \n\n Достигнут лимит:{base['warning']['limit'][a][b][1]}"
                            )
                        elif local_price < base["warning"]["limit"][a][b][0]:
                            bot_write(
                                user_id,
                                f"❗️🛑🛑🛑 \nЦена {local_token}:{local_price} \n\n Достигнут лимит:{base['warning']['limit'][a][b][0]}"
                            )
                    except KeyError:
                        print("*"*100+"\nMiss key\n"+"*"*100)


        for a in range(len(base["spam"]["token"])):
            user_id = base["id"][a]
            cooldown = base["spam"]["time"][a]
            if not user_id in base["black_list"] and (tick % cooldown == 0):
                print("ok")
                sms = ""
                try:
                    for i in range(len(base["spam"]["token"][a])):
                        sms += f"\nЦена {base['spam']['token'][a][i]}: {price[base['spam']['token'][a][i]]}$"
                    bot_write(user_id, sms)

                except KeyError:
                    print("*"*100+"\nMiss key\n"+"*"*100)
            else:
                print(f"No cooldown {a}")

        if tick >= 2880:
            tick = 0
        else:
            tick += 1

        print(f"Now tick: {tick}, check_price() go")

        """
        for a in token_base["tokens"]:

            for i in range(len(base["id"])):

                limit = base["limit"][i]

                if base["Question"]["warning"][i] and not id in base["black_list"] and a in base["token"][i]:
                    if price < limit[0]:
                        bot_write(base["id"][i], f"❗️🛑🛑🛑 \nЦена NOT:{price} \n\n Достигнут лимит:{limit[0]}")
                    elif price > limit[1]:
                        bot_write(base["id"][i], f"❕💸💸💸 \nЦена Not:{price} \n\n Достигнут лимит:{limit[1]}")

                if base["Question"]["spam"][i] and not id in base["black_list"] and a in base["token"][i]:
                    bot_write(base["id"][i], f"Not: {price}")

            print("OK")
        """
        sleep(60)
        print(tick)

if __name__ == "__main__":
    Thread(target=check_price).start()
    Thread(target=bot_main).start()


