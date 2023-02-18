from flask import render_template, flash, redirect, url_for, request
from jetskunk import app, db, bcr
from jetskunk.forms import RegisterForm, LoginForm
from jetskunk.db_models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home/')
def home():
    return render_template('index.html', title='Hey :)')


@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcr.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created :)', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcr.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in successfully :)', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('home'))
        elif not user:
            flash('There is no account connected to this email address', 'danger')
            return redirect(url_for('register'))
        else:
            flash('Email or password incorrect', 'warning')

    return render_template('login.html', title='Login', form=form)


@app.route('/account/')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))


quiz_dict = {
    1: 'usa_state_list.txt'
}


@app.route('/quiz/<int:quiz_number>')
def quiz(quiz_number):
    col = 5
    with open(f'{quiz_dict[quiz_number]}') as file:
        quiz_data = (file.read()).splitlines()
        length = len(quiz_data)
        row_number = round(length / col)

    return render_template('quiz.html', quiz_data=quiz_data, len=length, row_number=row_number, col_number=col)


