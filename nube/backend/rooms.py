import random
from bs4 import BeautifulSoup
import requests

class Rooms:
    def __init__(self):
        self.rooms = []
        self.url = 'https://sostaskillbox.it'

    def __repr__(self):
        return repr(self.rooms)

    def get_random_code(self):
        return ''.join([str(e) for e in random.choices(['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'], k=6)])

    def create_room(self, sid) -> str:
        room = {
            'name': self.get_random_code(),
            'owner': sid,
            'clients': 1,
            'actual': self.url
        }
        self.rooms.append(room)
        return room['name']

    def close_room(self, sid) -> str:
        room = [r for r in self.rooms if r['owner'] == sid][0]
        self.rooms.remove(room)
        return room['name']

    def join_room(self, room) -> bool:
        room = [r for r in self.rooms if r['name'] == room]
        if(len(room) != 1):
            return False
        room[0]['clients'] += 1
        return True

    def leave_room(self, room):
        room = [r for r in self.rooms if r['name'] == room][0]
        room['clients'] -= 1

    def clear(self):
        ret = self.rooms.copy()
        self.rooms.clear()
        return ret

    def get_url(self, room, num):
        if(not num.isdigit() or int(num)==0):
            return self.url
        

        room = [r for r in self.rooms if r['name'] == room][0]
        r = requests.get(room['actual'])
        soup = BeautifulSoup(r.content, 'html.parser')
        urls = []
        for img in soup.find_all('img', {'class':'elementor-animation-grow attachment-large size-large'}):
            link= img.find_parent('a')['href']
            if(link[0]=='/'):
                link=room['actual']+link
            elif(link[0]=='#'):
                link=room['actual']
            urls.append(link)
        return urls[int(num)-1]