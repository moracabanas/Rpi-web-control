from flask import Flask, request
from rooms import Rooms
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, close_room, send

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = Rooms()


@app.route('/')
def hello():
    return repr(rooms)


@app.route('/reset')
def reset():
    rs = rooms.clear()
    for room in rs:
        close_room(room['name'])
    return 'ok'


@socketio.on('create')
def on_create(data):
    sid = request.sid
    name = rooms.create_room(sid)
    join_room(name)
    res = {
        'state': 'create-room',
        'room': name,
    }
    send(str(res))


@socketio.on('close')
def on_close(data):
    sid = request.sid
    name = rooms.close_room(sid)
    res = {
        'state': 'close-room',
        'room': name,
    }
    send(str(res), room=name)
    close_room(name)


@socketio.on('join')
def on_join(data):
    room = data['room']
    sid = request.sid
    print(f'{sid} tries to join')
    res = {
        'state': '',
        'sid': sid,
        'room': '',
    }
    if(rooms.join_room(room)):
        res['state']='joined-room'
        res['room']=room
        join_room(room)
        print('{} join to room "{}".'.format(sid, room))
        send(str(res), room=room)
    else:
        res['state']='room-non-existent'
        print('{} can\'t join to room "{}".'.format(sid, room))
        send(str(res))


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    sid = request.sid
    rooms.leave_room(room)
    res = {
        'state': 'leaved-room',
        'sid': sid,
        'room': room,
    }
    leave_room(room)
    send(str(res), room=room)


@socketio.on('messages')
def send_to_room(data):
    room = data['room']
    message = data['message']
    sid = request.sid
    page = rooms.get_url(room, message)
    print(page)
    res = {
        'state': 'message',
        'sid': sid,
        'message': page,
    }
    send(str(res), room=room)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
    socketio.run(app, debug=True)

