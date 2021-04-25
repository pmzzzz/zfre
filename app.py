from datetime import timedelta

from flask import Flask
from flask import render_template, request, redirect, url_for, g, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user, LoginManager

from models import User, Bot

app = Flask(__name__, static_url_path='/')
app.config['SECRET_KEY'] = 'sauna*8'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# login_manager.login_message = u"请先登陆"

print(current_user, '89989')


@app.route('/')
def hello_world():
    print(hasattr(current_user, 'id'), 'hellobefor')
    if hasattr(current_user, 'id'):
        print(current_user.id, 'hello')
        # return redirect(url_for('manage'))

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # print(current_user.id, 'login')
    if request.method == 'POST':
        # 验证登陆？
        mail = request.form.get('email', None)
        password = request.form.get('password', None)
        print(password)
        if password == 'mmmm':

            user = User(user_id=1, password='123')
            login_user(user=user)
            return redirect(url_for('manage'))
        else:
            flash('账号或密码错误')
            return redirect(url_for('login'))
        pass

    return render_template('login.html')


bot = Bot(1, '123.com', 'se2448yb', '人社')
bots = [bot, bot, bot]


@app.route("/manage", methods=['GET', 'POST'])
@login_required
def manage():
    print(current_user.id, 'namage')
    if not current_user.id:
        flash('请先登录！')
        return redirect(url_for('login'))
    pass
    print()
    # bot = Bot(1, '123.com', 'se2448yb', '人社')
    # bots = [bot, bot, bot]
    return render_template('manage2.html', bots=enumerate(bots))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_bot(id):
    return str(id) + '正在修改'


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_bot(id):
    flash(str(id) + '被删了')
    bots.pop()
    return redirect(url_for('manage'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('再见')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
