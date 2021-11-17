from PyQt5.QtCore import QObject, pyqtSignal
import asyncio
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BCM_GPIO = [26,19,13,6]
GPIO_MAP = {
    26: "0",
    19: "1",
    13: "2",
    6: "3",
}

for i in BCM_GPIO:
    GPIO.setup(i, GPIO.IN, GPIO.PUD_UP)

class Worker(QObject):
    url_changed = pyqtSignal(str)
    room = pyqtSignal(str)
    message = pyqtSignal(str)
    event_detected = pyqtSignal(int)



    def __init__(self, window, sio):
        super().__init__()
        self.window = window
        self.sio = sio
        self.room_name = None
        self.callbacks()
        self.event_detected.connect(self.on_gpio_event)
        for i in BCM_GPIO:
            GPIO.add_event_detect(i, GPIO.FALLING, callback=self.event_detected.emit, bouncetime=200)
        


    def on_gpio_event(self, pin):
        # your code here!
        print(f"An event occurred on channel {pin}")
        if pin not in GPIO_MAP:
            raise ValueError(f"value pin {pin} not found. Use any in {BCM_GPIO}")
        self.trans_command(cmd=GPIO_MAP[pin])


    def callbacks(self):
        @self.sio.on('message')
        def message(data:str):
            resp = json.loads(data.replace("'",'"'))
            state = resp['state']
            print(f'{state} received with {data}')
            if(state == 'create-room'):
                self.room_name = resp['room']
                self.room.emit(resp['room'])
            elif(state == 'close-room'):
                pass
            elif(state == 'joined-room'):
                self.message.emit('{} joined'.format(resp['sid']))
            elif(state == 'leaved-room'):
                self.message.emit('{} left'.format(resp['sid']))
            elif(state == 'message'):
                self.message.emit('{} set page {}'.format(resp['sid'], resp['message']))
                self.url_changed.emit(resp['message'])
            # await sio.emit('response', {'response': 'my response'})

    def sio_connect(self):
        self.sio.connect('http://ec2-user@ec2-34-254-19-63.eu-west-1.compute.amazonaws.com:5000/')
        asyncio.run(self.get_push())
        self.sio.wait()

    async def get_push(self):
        self.sio.emit('create', {})
        while True: # Wait
            page = input('command: ')
            self.trans_command(page)

    def trans_command(self, cmd:str):
        self.sio.emit('messages', {
            'room': self.room_name, 
            'message': cmd
        })
        print(cmd)

    def run(self):
        self.sio_connect()
