from flask import Flask, render_template, redirect, abort, flash
from flask_login import LoginManager, login_user, logout_user, current_user

from forms import RegisterForm, LoginForm, QuoteInput
from utils import *
from app import app


# Custom 404 template
def not_found(e):
    return render_template('404.html'), 404

# Registering custom 404
app.register_error_handler(404, not_found)


@app.route('/')
def main_page():
    # Redirect to profile if the user is authenticated
    if current_user.is_authenticated:
        return redirect(f'/user/{current_user.usertag}')

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #Redirect to / if the user is logged in
    if current_user.is_authenticated:
        return redirect('/')
    
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username = register_form.username.data
        usertag = register_form.usertag.data
        password = register_form.password.data

        if validate_signup(username):
            u = register_user(username, usertag, password)
            login_user(u)
            return redirect(f'/user/{usertag}')

    return render_template('signup.html', form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        return redirect('/')

    login_form = LoginForm()
    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data
        remember_me = login_form.remember_me.data

        if validate_login(username, password):
            user = find_user(username)
            login_user(user, remember=remember_me)
            return redirect(f'/user/{username}')
        else:
            flash('Invalid user credentials.')

    return render_template('login.html', form=login_form)


@app.route('/delete/<int:quote_id>')
def remove_quote(quote_id):
    if current_user.is_authenticated:

        quote = current_user.quotes.filter_by(id=quote_id).first()
        current_user.remove_quote(quote)
        return redirect('/')

    # If the quote doesn't exist
    return abort(404)


@app.route('/follow/<string:username>')
def follow(username):
    u = find_user(username)

    if not current_user.is_authenticated:
        return redirect('/login')
    elif not u:
        abort(404)

    current_user.follow(u)
    return redirect(f'/user/{username}')


@app.route('/unfollow/<string:username>')
def unfollow(username):
    u = find_user(username)

    if not u or not current_user.is_authenticated:
        abort(404)

    current_user.unfollow(u)
    return redirect(f'/user/{username}')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/user/<string:usersearch>', methods=["GET", "POST"])
def search_page(usersearch):
    u = find_user(usersearch)
    if not u:
        abort(404)

    quote_input = QuoteInput()

    if quote_input.validate_on_submit():
        create_quote(current_user, quote_input.quote_content.data)

    suggestions = user_suggestions(usersearch, 5)

    # Getting the quotes reversed for chronologic view
    quotes = u.quotes_[::-1]

    return render_template('profile.html', 
                            quotes=quotes,
                            user=u,
                            quote_input=quote_input,
                            user_pic=u.profile_pic,
                            rec_users=suggestions,
                            usertag=u.usertag, 
                            username=u.username,
                            following=u.total_following,
                            followers=u.total_followers,
    )
