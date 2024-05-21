from modules.tg_bot import *
from modules.spot_price import *

from threading import Thread
from time import sleep

limit = [0.00657, 0.0068]

def check_price():
    while True:
        price = float(get_price()["buy"])
        base = update_date()

        for i in range(len(base["id"])):
            limit = base["limit"][i]

            if base["Question"]["warning"][i] and not id in base["black_list"]:
                if price < limit[0]:
                    bot_write(base["id"][i], f"❗️🛑🛑🛑 \nЦена NOT:{price} \n\n Достигнут лимит:{limit[0]}")
                elif price > limit[1]:
                    bot_write(base["id"][i], f"❕💸💸💸 \nЦена Not:{price} \n\n Достигнут лимит:{limit[1]}")
            if base["Question"]["spam"][i] and not id in base["black_list"]:
                bot_write(base["id"][i], f"Not: {price}")
        print("OK")

        sleep(60)


if __name__ == "__main__":
    Thread(target=check_price).start()
    Thread(target=bot_main).start()
