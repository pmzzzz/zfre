from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import render_template, request, redirect, url_for, g, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from db import Mysql
from models import User, Bot
from utils import load_bot
from multiprocessing import Process
from threading import Thread

app = Flask(__name__, static_url_path='/')
app.config['SECRET_KEY'] = 'sauna*8'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# 装载所有机器人,:
def load_all_bot():
    pri = Mysql()
    pri.cursor.execute('select id,url,secret,name,status,kw,period,send_time,user_id,create_time,site from bot')
    ppp = pri.cursor.fetchall()
    pri.end()
    return {i[0]: load_bot(i) for i in ppp}


global_bots = load_all_bot()
global_running_scheduler = {}

# 开启非阻塞 存入scheduler
for k, v in global_bots.items():
    if v.status == 1:
        h, m, s = v.send_time.split(':')
        scheduler = BackgroundScheduler()
        scheduler.add_job(v.run, 'cron', hour=h, minute=m, second=s)
        global_running_scheduler[k] = scheduler
        scheduler.start()


# login_manager.login_message = u"请先登陆"

# print(current_user, '89989')


@app.route('/')
def hello_world():
    print(hasattr(current_user, 'id'), 'hellobefor')
    if hasattr(current_user, 'id'):
        print(current_user.id, 'hello')
        # return redirect(url_for('manage'))
    print('hahahah')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # print(current_user.id, 'login')
    if request.method == 'POST':
        # 验证登陆？
        mail = request.form.get('email', None)
        password = request.form.get('password', None)
        print(password)
        # if password == 'mmmm':
        #
        #     user = User(user_id=1, password='123')
        #     login_user(user=user)
        #     return redirect(url_for('manage'))
        mysql = Mysql()
        tem = mysql.query_mail(mail)

        print('tem', tem)
        if tem:
            tem = mysql.query_mail(mail)[0]
            if tem[2] == password:
                print(tem[1], 'tem1')
                user = User(user_id=tem[0], password=password, mail=mail, name=tem[1])
                print(user, 'cccccc')
                login_user(user=user)
                print(current_user.name, 'wcwcwcwwccwwcw')
                flash('欢迎你：{}'.format(user.name))
                mysql.end()
                return redirect(url_for('manage'))
            else:
                flash('密码错误')
                mysql.end()
                return redirect(url_for('login'))
        else:
            flash('用户不存在')
            mysql.end()
            return redirect(url_for('login'))
    return render_template('login.html')


# name, url, secret, bot_id,user_id, status, kw='大数据', site=1, period=1, send_time='09:00'
# bot = Bot('测试', '123.com', 'se2448yb', 1, 100, 1, '大数据', 1, 1, '09:00')
# bots = [bot, bot, bot]


@app.route("/manage", methods=['GET', 'POST'])
@login_required
def manage():
    global global_bots
    # global_bots =
    print(current_user.id, 'manage')
    if not current_user.id:
        flash('请先登录！')
        return redirect(url_for('login'))
    else:
        print(current_user.password)
        mysql = Mysql()
        bots = mysql.query_bots_by_user_id(current_user)
        # if len(bots) >= 1:
        #     bots = [Bot(bot_id=bot[0], url=bot[1], secret=bot[2], name=bot[3], status=bot[4], kw=bot[5], period=bot[6],
        #                 send_time=bot[7], user_id=bot[8], create_time=bot[9], site=bot[10]) for bot in bots]
        if len(bots) >= 1:
            bots = [j for i, j in global_bots.items() if i in [x[0] for x in bots]]
        else:
            pass
        # print(bots[0].status, 'dsdwedei问问去')
        # bot = Bot(1, '123.com', 'se2448yb', '人社')
        # bots = [bot, bot, bot]
        #     name, url, secret, bot_id, user_id, status, kw = '大数据', site = '人设', period = 1, send_time = '09:00'
        return render_template('manage2.html', bots=enumerate(bots))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mysql = Mysql()
        email = request.form.get('email', None)
        tem = mysql.query_mail(email)
        print(tem, 'ddddddddddd')
        if tem:
            flash('邮箱已注册')
            return redirect(url_for('register'))
        elif request.form.get('password') == request.form.get('password1'):
            flash('注册成功')
            redirect(url_for('login'))
        else:
            flash('密码不一致')
    return render_template('register.html')


@app.route('/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_bot(id):
    return str(id) + '正在修改'


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_bot(id):
    bot = global_bots[id]
    bot.status = 0
    global_bots.pop(id)
    ms = Mysql()
    sql = 'delete from bot where id = %s'
    ms.cursor.execute(sql, [id])
    ms.content.commit()
    flash(str(id) + '被删了')

    return redirect(url_for('manage'))


@app.route('/add_bot', methods=['POST'])
@login_required
def add_bot():
    print('sdsds')
    # print(request.form.to_dict())
    site = '、'.join(request.form.getlist('sites'))
    mode = request.form.get('mode')
    url = request.form.get('url', None)
    secret = request.form.get('secret')
    status = 0
    kw = request.form.get('kw')
    send_time = request.form.get('send_time')
    name = request.form.get('name')

    print(request.form.to_dict())
    # print(url)
    temp = Bot(bot_id=-1, site=site, send_time=send_time, period=mode, url=url, user_id=current_user.id, status=status,
               secret=secret, kw=kw, name=name)
    print(temp)
    mss = Mysql()
    mss.add_bot(temp)
    del temp
    bot = load_bot(mss.query_all_bot()[-1])
    global_bots[bot.id] = bot
    return redirect(url_for('manage'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('再见')
    return redirect(url_for('login'))


@app.route('/bot_info/<int:id>')
@login_required
def bot_info(id):
    mysql = Mysql()
    # if mysql:
    #     x = list(filter(lambda x: x[0] == id, mysql.query_all_bot()))[0]
    x = list(filter(lambda y: y[0] == id, mysql.query_all_bot()))[0]
    mysql.end()
    return render_template('info.html', x=x)


@app.route('/bot_open/<int:id>')
@login_required
def bot_open(id):
    bot = global_bots[id]
    bot.status = 1
    # global_bots[id] = bot
    # 修改数据库
    ms = Mysql()
    ms.cursor.execute('update bot set status=1 where id=%s', [bot.id])
    ms.content.commit()
    ms.end()
    hr, mn, sc = bot.send_time.split(':')
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(bot.run, 'cron', hour=hr, minute=mn, second=sc)
    global_running_scheduler[bot.id] = scheduler1
    scheduler1.start()
    print('非阻塞')
    print(global_running_scheduler)
    return redirect(url_for('manage'))


@app.route('/bot_close/<int:id>')
@login_required
def bot_close(id):
    global_bots[id].status = 0
    # 修改数据库
    ms = Mysql()
    ms.cursor.execute('update bot set status=0 where id=%s', global_bots[id].id)
    ms.content.commit()
    ms.end()
    global_running_scheduler[id].shutdown()
    print(global_running_scheduler, '关闭')
    return redirect(url_for('manage'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050, processes=True)
