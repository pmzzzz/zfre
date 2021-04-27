from models import Bot
import os

url = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=a2b1bb1046f9b876111599ed058dc2f9d1195db270a74fddde49d0b3aebdbaa4 '
secret = 'SEC324fa30727ff0505cc3beb25f92fa32e92f58423082f31f7b190c4f9131ed65f'

bot = Bot(name='人社', url=url, secret=secret, bot_id=1, user_id=100, status=0,kw='大数据',period='week',send_time='15:33:00',site='人社、经信委、科委')
bot.kw = '，'
x = bot.test()
# os.getgid(x)

# from threading import Thread
# import time
#
# class CountdownTask:
#     def __init__(self):
#         self._running = True
#
#     def terminate(self):
#         self._running = False
#
#     def run(self, n):
#         while self._running and n > 0:
#             print('T-minus', n)
#             n += 1
#             time.sleep(1)
#
#
# c = CountdownTask()
# t = Thread(target=c.run, args=(10,))
# t.start()
# time.sleep(5)
# c.terminate()  # Signal termination
# t.join()  # Wait for actual termination (if needed)
