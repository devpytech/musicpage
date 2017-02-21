# Python powered music controlling startpage

![A screenshot](http://www.devpy.me/content/images/2017/02/ezgif.com-video-to-gif--2-.gif)

I had the idea of making a start page that could control my music. This is the result; it uses bottle py and a websocket to update what's playing in real time.

Dependencies:

* [Playerctl](https://github.com/acrisci/playerctl)
* bottle (pip)
* bottle-websocket (pip)

I had to use Python2 because gevent (the websocket) unfortunately does not support Python3.
