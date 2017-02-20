from bottle import route, run, template
import numpy as np
import os

@route('/')
def index():
    head = '''
<html>
<head>
<title>Start Page</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tachyons/4.6.2/tachyons.css" />
</head>
<body>
'''
    display = '''
<div class="db center black link" style="width: 182px;">
  <img class="db ba b--black-10"/
       alt="Frank Ocean Blonde Album Cover"
       src="%s">

  <dl class="mt2 lh-copy">
    <dt class="clip">Title</dt>
    <dd class="ml0 fw9">%s</dd>
    <dt class="clip">Artist</dt>
    <dd class="ml0 gray">%s</dd>
  </dl>
</div>''' % (os.popen("playerctl metadata mpris:artUrl").read(), os.popen("playerctl metadata title").read(), os.popen("playerctl metadata artist").read())

    end = '</body>'
    return head + display + os.popen("playerctl metadata mpris:length") + end

run(host='localhost', port=8080)
