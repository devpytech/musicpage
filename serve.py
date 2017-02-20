#!/usr/bin/env python2
from bottle import route, run, request, get, post, static_file
import gi
gi.require_version('Playerctl', '1.0')
from gi.repository import GLib, GObject, Playerctl
from subprocess import Popen
import sys
import os

Popen([sys.executable, './sendup.py']) #run the websocket script (used to update info)

############
# SETTINGS
############

links = [['DevPy','http://DevPy.me'],['Reddit','http://Reddit.com'],['Google','http://Google.com']]

theme = 'dark' #light or dark

############
# /SETTINGS
############

if theme == 'dark':
    bgc = '#222'
    fgc = 'rgba(255,255,255,0.6)'
    bw = 'gray'
else:
    bgc = '#fff'
    fgc = '#111'
    bw = 'black'

for x in range(len(links)):
    links[x] = '<a class="db link no-underline underline-hover '+bw+'" href="'+links[x][1]+'">'+links[x][0]+'</a>'

linkhtml = '''<div class="db center" style="width: 182px;"><div class="mt4 lh-copy">'''

for x in links:
    linkhtml += x

linkhtml += '''</div></div>'''

@get('/') # or @route('/login')
def index():
    return '''
<html>
<head>
<title>Start Page</title>
<link rel="stylesheet" href="/static/tachyons.css" />
<link rel="stylesheet" href="/static/font-awesome.min.css" />
<style>
/* fallback */
@font-face {
  font-family: 'Material Icons';
  font-style: normal;
  font-weight: 400;
  src: local('Material Icons'), local('MaterialIcons-Regular'), url(/static/mat.woff2) format('woff2');
}

.material-icons {
  cursor: pointer;
  font-family: 'Material Icons';
  font-weight: normal;
  font-style: normal;
  font-size: 30px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-feature-settings: 'liga';
  -webkit-font-smoothing: antialiased;
}

.material-icons.md-light { color: rgba(0, 0, 0, 0.54); }

.material-icons.md-dark { color: rgba(255, 255, 255, 1); }
</style>
</head>
<body style="background-color:'''+bgc+'''">

<div style="position:relative; top: 35%%; transform: translateY(-50%%); ">
<div class="mt4 db center black link" style="width: 178px;">
  <img id="img" style="width:180px;height:178px;background-color:#222;"class="db ba b--black-10" src="%s">

  <dl class="mt2 lh-copy">
    <dt class="clip">Title</dt>
    <dd id="title" class="ml0 fw9" style="color:''' % (os.popen("playerctl metadata mpris:artUrl").read())+fgc+'''">%s</dd>
    <dt class="clip">Artist</dt>
    <dd id="artist" class="ml0 gray">%s</dd>
  </dl>

  <div style="text-align:center;color:''' % (Playerctl.Player().get_title(), Playerctl.Player().get_artist())+fgc+'''">
    <a onclick="previous();" style="float:left;"><i class="material-icons md-'''+theme+'''">skip_previous</i></a>
    <a onclick="toggle();"><i id ="stateicon" style="width:32px;" class="material-icons md-'''+theme+'''">pause_arrow</i></a>
    <a onclick="next();" style="float:right;"><i class="material-icons md-'''+theme+'''">skip_next</i></a>
  </div>
</div>

''' + linkhtml + '''
</div>
<script src="/static/jquery-3.1.1.min.js"></script>
<script type="text/javascript">
var ws;
ws = new WebSocket("ws://0.0.0.0:7000/websocket");

ws.onopen = function (evt) {
  ws.send("Connected");
};

ws.onclose = function (evt) {
  ws.send("Closed");
};

ws.onmessage = function (evt) {
    var array = evt.data.split(',');
    if (array.length == 4) {
        console.log(array);
        $("#img").attr("src", array[0]);
        $("#title").text(array[1]);
        $("#artist").text(array[2]);
        if (array[3] === 'Playing') {
            $('#stateicon').text('pause');
        } else {
            $('#stateicon').text('play_arrow');
        }
        ws.send("Updated");
    } else {
        ws.send("OK.")
    }
};

</script>
<script>
function next() {
    $.post('/next')
    return false;
}

function previous() {
    $.post('/previous')
    return false;
}

function toggle() {
    $.post('/toggle');
    return false;
}
</script>
</body>
</html>
'''
@post('/next')
def next_song():
    Playerctl.Player().next()

@post('/previous')
def next_song():
    Playerctl.Player().previous()

@post('/toggle')
def next_song():
    Playerctl.Player().play_pause()

@post('/status')
def is_playing():
    return Playerctl.Player().get_property("status")

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/robert/Documents/Python/StartPage')

@route('/fonts/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/robert/Documents/Python/StartPage')

run(host='0.0.0.0', port=8080)
