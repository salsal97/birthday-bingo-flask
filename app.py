import re
import os
import random 
import json
from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)

# using Flask's app.route decorator to map the URL route / to that function:
# @app.route("/")
# def home():
#     return render_template("layout.html")
@app.route("/")
def home():
    no_of_columns=4
    image_path='static/index/'
    image_list=os.listdir(image_path)
    image_lists=[]

    for _ in range (0, no_of_columns):
        temp = image_list[:]
        random.shuffle(temp)
        image_lists.append(temp)
    
    image_path='index/'

    return render_template("index.html",
    image_lists=image_lists,
    image_path=image_path
    )

@app.route("/game")
def game():
    with open('static/bingo.json') as f:
        data = json.load(f)
    abort=False
    for card in data['bingo_cards']:
        if card['type'] == "photo":
            # Check if photo exists
            if (not os.path.isfile(card['photo_cropped'])):
                print(card['photo_cropped']+" is not a file!!!")
                abort=True
            if (not os.path.isfile(card['photo_full'])):
                print(card['photo_full']+" is not a file!!!")
                abort=True
    if abort:
         raise RuntimeError('Aborting! Fix file structure')

    return render_template("bingo.html",
    data=data)

@app.route("/prize")
def prize():
    with open('static/bingo.json') as f:
        data = json.load(f)
    return render_template("prize.html",
    data=data)

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
