import os
import sys
from flask import Flask, request, render_template, send_from_directory
app = Flask(__name__)
import requests

appname = "trello-focus"
appkey = os.environ.get('APPKEY')
appsecret = os.environ.get('APPSECRET')
appoauth = "https://"+appname+".herokuapp.com/oauth"

         
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', oauth_url="https://trello.com/1/authorize?expiration=never&name="+appname+"&scope=read&response_type=token&key="+appkey+"&return_url="+appoauth)


@app.route('/oauth')
def oauthr():
    return render_template('redir.html')
    

@app.route('/focus')
def focus():
    token = request.args.get('token', type=str)
    embed = request.args.get('embed', "false", type=str)

    x = requests.get("https://api.trello.com/1/members/me/boards/",
                      params = {'key': appkey, 'token': token})
    boards = []
    bresp = x.json()
    for bitem in bresp:
      #if bitem["closed"] == "false":
        board = {'id': bitem["id"], 'name': bitem["name"], 'url': bitem["url"], 'cards': []}
        x = requests.get("https://api.trello.com/1/boards/"+board["id"]+"/",
                         params = {'cards':'all', 'key': appkey, 'token': token})
        cresp = x.json()
        for citem in cresp["cards"]:
          include = False
          for label in citem["labels"]:
            if label["name"] == "FOCUS":
              include = True          
          if include:
            board["cards"].append({'id': citem["id"], 'url': citem["shortUrl"], 'name': citem["name"]})        
        if len(board["cards"]) > 0:
          boards.append(board)

    return render_template('board.html', boards=boards, token=token, embed=(False if embed=="false" else True))
