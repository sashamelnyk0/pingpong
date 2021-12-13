from tkinter import *
import random
import time
import socket
import threading


root = Tk()
root.title('middle')
root.geometry('470x700')  
canv = Canvas(root, bg='green')
canv.pack(fill=BOTH, expand=1)
root.resizable(width=False, height=False)


host = '192.168.0.133'		
port = 0
server = ('192.168.0.133', 3332)     
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(False)
shutdown = False
data = ''
s.sendto('ball.py'.encode('utf-8'), server)

class ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.position = [self.x, self.y]
        self.map = ''
        self.lin = [self.map, self.position]
        self.r = 12
        self.vx = 0
        self.vy = 0
        self.goal = 0
        self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='yellow')

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.position[0] = self.x
        self.position[1] = self.y
        active_wall = list(set(canv.find_withtag('wall')) & set(
            canv.find_overlapping(self.x - self.r * 0.7, self.y - self.r * 0.7, self.x + self.r * 0.7,
                                  self.y + self.r * 0.7)))
        if active_wall:
            if 'x' in canv.gettags(active_wall[0]):
                self.vx = -self.vx
            if 'y' in canv.gettags(active_wall[0]):
                self.vy = -self.vy
                x1, y1, x2, y2 = canv.coords(active_wall[0])
                xc = (x1 + x2) / 2
                w = abs(x1 - x2)
                self.vx += (self.x - xc) / w * 10
        self.paint()
        lines = canv.find_overlapping(self.x - self.r * 0.7, self.y - self.r * 0.7, self.x + self.r * 0.7,
                                      self.y + self.r * 0.7)
        if len(lines) > 1:
            if "g1" in canv.gettags(lines[1]):
                self.goal = 'g1'
                self.kill()
            if "g2" in canv.gettags(lines[1]):
                self.goal = 'g2'
                self.kill()
            if self.goal == '1':
                self.kill()
            if self.goal == '2':
                self.kill()

    def kill(self):
        global game
        game = 1
        if self.goal == 'g1':
            self.map = '[Ball -> Gamer1] :: '
            self.lin[0] = self.map
            self.lin[1] = self.position
            s.sendto(f'{self.lin[0]}${self.lin[1][0]}${self.lin[1][1]}'.encode('utf-8'), server)
            self.x = 235  
            self.y = 800  
            self.vx = 0
            self.vy = 0
            self.goal = 0
        if self.goal == 'g2':
            self.map = '[Ball -> Gamer2] :: '
            self.lin[0] = self.map
            self.lin[1] = self.position
            s.sendto(f'{self.lin[0]}${self.lin[1][0]}${self.lin[1][1]}'.encode('utf-8'), server)
            self.x = 235  
            self.y = 800  
            self.vx = 0
            self.vy = 0
            self.goal = 0
        self.paint()

    def paint(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)


class gamer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 2 
        self.v = 4 
        self.d = 60  
        self.mode = ''
        self.score = 0  
        self.xy_score = (0, 0)  
        self.id = canv.create_rectangle(self.x - self.w, self.y - self.d, self.x + self.w, self.y + self.d,
                                        fill='white', tags=('wall', 'x'))
        self.id_score = canv.create_text(0, 0, text='', font='Tahoma 24', fill='white')

    def paint(self):
        canv.coords(self.id, self.x - self.w, self.y - self.d, self.x + self.w, self.y + self.d)
        canv.coords(self.id_score, self.xy_score[0], self.xy_score[1])
        canv.itemconfig(self.id_score, text=self.score)

    def move(self):
        if self.mode == 'top' and self.y > (115 - self.d // 2):
            self.y -= self.v
        elif self.mode == 'down' and self.y < (550 - self.d // 2):
            self.y += self.v
        self.paint()



def rand(side=None):
    ex = True
    lin_v = []  
    rand_v = 0
    if side is True:    
        while ex:
            randing = random.randint(0, 1)
            if randing == 0:
                rand_v = 10
            elif randing == 1:
                rand_v = -10
            lin_v.append(rand_v)
            if len(lin_v) == 2:
                if lin_v != [4, 4] or lin_v != [4, -4]:
                    ex = False
                else:
                    lin_v = []
        return lin_v
    elif side is False:     
        while ex:
            randing = random.randint(0, 1)
            if randing == 0:
                rand_v = 4
            elif randing == 1:
                rand_v = -4
            lin_v.append(rand_v)
            if len(lin_v) == 2:
                if lin_v != [-4, -4] or lin_v != [-4, 4]:
                    ex = False
                else:
                    lin_v = []
        return lin_v
    else:                   
        while ex:
            randing = random.randint(0, 1)
            if randing == 0:
                rand_v = 4
            elif randing == 1:
                rand_v = -4
            lin_v.append(rand_v)
            if len(lin_v) == 2:
                ex = False
        return lin_v




b = ball()
b.x = 235
b.y = 350
v = rand()
b.vx = v[0]    
b.vy = v[1]    
game = 0



canv.create_line(2, 10, 2, 690, width=2, fill='white', tags='g1')   
canv.create_line(468, 10, 468, 689, width=2, fill='white', tags='g2')  
 

canv.create_line(2, 11, 469, 11, width=10, fill='white', tag=('wall', 'y'))
canv.create_line(2, 689, 469, 689, width=10, fill='white', tag=('wall', 'y'))    




def key_press(event):
    global game

    if event.keycode == 32:   
        game = 1


root.bind('<Key>', key_press)




def receving(name, sock):   
    global data
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                data = data.decode('utf-8')
                print(data)

                time.sleep(0.2)
        except:
            pass


print('--- [ Ball ] ---')
print(f'IP :: {host}\n')
rT = threading.Thread(target=receving, args=('RecvThread', s))
rT.start()


while 1:
    if game:
        b.move()
    time.sleep(0.02)
    canv.update()

    
    if '$' in data:
        data_lin = data.split('$')  
        data = data.replace('$', '')
        data_x = data_lin[1]
        data_y = data_lin[2]
        if data_lin[0] == '[Gamer1 -> Ball] :: ':
            data_x = 18
            b.x = float(data_x)
            b.y = float(data_y)
            b.vx = 10
            b.vy = 10
            b.kill()
        elif data_lin[0] == '[Gamer2 -> Ball] :: ':
            data_x = 452
            b.x = float(data_x)
            b.y = float(data_y)
            b.vx = -10
            b.vy = 10
            b.kill()
    elif data == '1':
        data = ''
        b.x = 235
        b.y = 350
        v = rand(False)
        b.vx = v[0]
        b.vy = v[1]
        b.kill()
    elif data == '2':
        data = ''
        b.x = 235
        b.y = 350
        v = rand(True)
        b.vx = v[0]
        b.vy = v[1]
        b.kill()
    

root.mainloop()
rT.join()
s.close()