#!/usr/bin/env python2
from bottle.ext.websocket import GeventWebSocketServer
import gi
gi.require_version('Playerctl', '1.0')
from gi.repository import GLib, GObject, Playerctl
from bottle.ext.websocket import websocket
from geventwebsocket.exceptions import WebSocketError
from bottle import run, get
import threading
import os
from urllib import unquote
from gevent import monkey
monkey.patch_all()

print("starting websocket")

@get('/websocket', apply=[websocket])
def echo(ws):
    #print([obj for obj in gc.get_objects() if isinstance(obj, greenlet)])
    #gevent.killall([obj for obj in gc.get_objects() if isinstance(obj, greenlet)])
    print("connected")
    if Playerctl.Player().get_properties('player-name')[0] == 'vlc':
        imgpath = unquote(os.popen("playerctl metadata mpris:artUrl").read()).replace('file://', '')
        with open('artwork.jpg', 'wb') as artwork:
            artwork.write(open(imgpath, 'rb').read())
        img = '/static/artwork.jpg?{0}'.format(Playerctl.Player().get_title())
    else:
        img = os.popen("playerctl metadata mpris:artUrl").read()
    ws.send('%s,%s,%s,%s' % (img, Playerctl.Player().get_title(), Playerctl.Player().get_artist(), Playerctl.Player().get_property("status")))
    def on_track_change(player, e):
        try:
            if Playerctl.Player().get_properties('player-name')[0] == 'vlc':
                imgpath = unquote(os.popen("playerctl metadata mpris:artUrl").read()).replace('file://', '')
                with open('artwork.jpg', 'wb') as artwork:
                    artwork.write(open(imgpath, 'rb').read())
                img = '/static/artwork.jpg?{0}'.format(Playerctl.Player().get_title())
            else:
                img = os.popen("playerctl metadata mpris:artUrl").read()
            ws.send('%s,%s,%s,%s' % (img, Playerctl.Player().get_title(), Playerctl.Player().get_artist(), Playerctl.Player().get_property("status")))
        except WebSocketError:
            player.stop()
            loop.quit()
            ws.close()

    player = Playerctl.Player()
    player.on('metadata', on_track_change)
    #GLib.timeout_add(100, checksocks, ws)
    #print GLib.MainLoop().get_context().iteration()

    loop = GLib.MainLoop()
    #threading.Thread(target=checksocks, args=(player,loop)).run()
    loop.run()
    print("CLOSED!")


run(host='0.0.0.0', port=7000, server=GeventWebSocketServer)
