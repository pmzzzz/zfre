from datetime import timedelta

from flask import Flask
from flask import render_template, request, redirect, url_for, g, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from db import Mysql
from models import User, Bot

app = Flask(__name__, static_url_path='/')
app.config['SECRET_KEY'] = 'sauna*8'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# 装载所有机器人, id:机器人实例
pri = Mysql()
pri.cursor.execute('select id,url,secret,name,status,kw,period,send_time,user_id,create_time,site from bot')
ppp = pri.cursor.fetchall()
pri.end()
global_bots = {i[0]:Bot(bot_id=i[0],url=i[1],secret=i[2],name=i[3],status=i[4],
                        kw=i[5],period=i[6],send_time=i[7],user_id=i[8],create_time=i[9],site=i[10]
                        ) for i in ppp
               }


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
    print(current_user.id, 'manage')
    if not current_user.id:
        flash('请先登录！')
        return redirect(url_for('login'))
    else:
        print(current_user.password)
        mysql = Mysql()
        bots = mysql.query_bots_by_user_id(current_user.id)
        # if len(bots) >= 1:
        #     bots = [Bot(bot_id=bot[0], url=bot[1], secret=bot[2], name=bot[3], status=bot[4], kw=bot[5], period=bot[6],
        #                 send_time=bot[7], user_id=bot[8], create_time=bot[9], site=bot[10]) for bot in bots]
        if len(bots) >= 1:
            bots = [j for i,j in global_bots.items() if i in [x[0] for x in bots]]
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
    flash(str(id) + '被删了')

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

    return render_template('info.html', x=x)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
