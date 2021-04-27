from models import User, Bot


def load_bot(i):
    if i:
        return Bot(bot_id=i[0], url=i[1], secret=i[2], name=i[3], status=i[4],
                   kw=i[5], period=i[6], send_time=i[7], user_id=i[8], create_time=i[9], site=i[10]
                   )


def load_user():
    pass
