from flask import Flask, request, render_template, make_response, url_for, redirect, send_from_directory
import json
import requests
from csutils import *
import os

app = Flask(__name__)

# Get cookies, lot of this is based on Fireblend's squirdle app which is very cool
def get_cookie_data(daily=''):
    # Cookies for daily session are prefixed with 'd_'
    prefix = 'd_' if daily else ''
    secret = request.cookies.get(prefix + 'secret_item')
    attempts = int(request.cookies.get(prefix + 't_attempts'))
    return secret, attempts

def show_game_state(is_daily):
    day = getDayCount() if is_daily else None
    secret, attempts = get_cookie_data(daily=is_daily)
    secret_split = secret.split("///")
    secret_present = secret_split[0] + " (" + secret_split[1] + ")"
    items = getItemsJson()
    secret_thumb = items[secret_split[0]]["exterior"][secret_split[1]]["url"]
    imgs = [url_for('static', filename=f'{x}.png') for x in ['correct', 'up', 'down', 'wrong']]

    return render_template('daily.html' if is_daily else 'endless.html', items=items, day=day,
        secret=secret, secret_present=secret_present, secret_thumb=secret_thumb, attempts=attempts, im=imgs)

# Sets cookies for new games
def handle_new_game(is_daily):
    expire_date = None
    # 24h, since daily
    if is_daily:
        expire_date = datetime.combine(datetime.date(datetime.now()-timedelta(hours=10)),
            datetime.min.time())+timedelta(days=1,hours=10)
    else:
        expire_date = datetime.date(datetime.now())+timedelta(days=7)

    prefix = 'd_' if is_daily else ''

    # Set cookies
    resp = make_response(redirect(url_for('daily' if is_daily else 'endless')))
    resp.set_cookie(prefix + 'secret_item', get_skin(daily=is_daily), expires=expire_date)
    resp.set_cookie(prefix + 't_attempts', '8', expires=expire_date)
    return resp

@app.route('/')
def daily():
    # Set cookies if a new game is requested
    if not 'd_secret_item' in request.cookies:
        return handle_new_game(is_daily=True)
    return show_game_state(is_daily=True)

@app.route('/endless')
def endless():
    # Set cookies if a new game is requested
    if not 'secret_item' in request.cookies:
        return handle_new_game(is_daily=False)
    return show_game_state(is_daily=False)


# @app.route('/')
# def index():
#     # Set cookies if a new game is requested
#     if not 'secret_item' in request.cookies:
#         return handle_new_game(is_daily=False)
#     return show_game_state(is_daily=False)

# @app.route('/daily')
# def daily():
#     # Set cookies if a new game is requested
#     if not 'd_secret_item' in request.cookies:
#         return handle_new_game(is_daily=True)
#     return show_game_state(is_daily=True)

@app.route('/daily')
def dailyRedirect():
    return redirect('/', code=302)

@app.route('/dev')
def dev():
    # Redirect to a writeup I did on the project
    return redirect("https://painted-coach-e77.notion.site/Creating-CS-GOrdle-9f397ab9e6bd4df69793811e55cc9b83", code=302)

@app.route('/final_update')
def finalUpdate():
    # Redirect to maybe final update
    return redirect("https://painted-coach-e77.notion.site/CS-Gordle-s-Probably-Final-Update-9b6316c998db4b4f9c25da2bef91a65c", code=302)