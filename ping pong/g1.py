from tkinter import *
import time
import socket
import threading


root = Tk()
root.title('left')
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
s.sendto('g1.py'.encode('utf-8'), server)




class ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.position = [self.x, self.y]
        self.map = ''
        self.status = ''
        self.lin = [self.map, self.position, self.status]
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

    def kill(self):
        global game
        game = 1
        if self.goal == 'g1':  
            self.map = '[Ball -> Goal_g1] :: '
            self.lin[0] = self.map
            self.status = '!Goal to Gamer1!'
            self.lin[2] = self.status
            s.sendto(f'{self.lin[0]}&{self.lin[2]}'.encode(), server)
            self.x = 235
            self.y = 800
            self.vx = 0
            self.vy = 0
            self.goal = 0
        elif self.goal == 'g2':  
            self.map = '[Gamer1 -> Ball] :: '
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
        self.w = 3
        self.v = 5  
        self.d = 60 
        self.mode = ''
        self.score = 0  
        self.xy_score = (0, 0)  
        self.id = canv.create_rectangle(self.x - self.w, self.y - self.d, self.x + self.w, self.y + self.d,
                                        fill='red', tags=('wall', 'x'))
        self.id_score = canv.create_text(0, 0, text='', font='Tahoma 24', fill='white')

    def paint(self):
        canv.coords(self.id, self.x - self.w, self.y - self.d, self.x + self.w, self.y + self.d)
        canv.coords(self.id_score, self.xy_score[0], self.xy_score[1])
        canv.itemconfig(self.id_score, text=self.score)

    def move(self):  
        if self.mode == 'top' and self.y > (115 - self.d // 2):
            self.y -= self.v
        elif self.mode == 'down' and self.y < (645 - self.d // 2):
            self.y += self.v
        self.paint()




b = ball()
b.x = 235
b.y = 800
b.vx = 1000
b.vy = 1000

canv.create_line(10, 10, 10, 689, width=2, fill='white', tags='g1')   
canv.create_line(468, 10, 468, 689, width=2, fill='white', tags='g2')  

canv.create_line(9, 11, 471, 11, width=10, fill='white', tag=('wall', 'y'))  
canv.create_line(9, 689, 471, 689, width=10, fill='white', tag=('wall', 'y'))    


g1 = gamer()
g1.x = 20  
g1.y = 300   
g1.paint()
g1.xy_score = (235, 80)  # Рахунок
game = 1

def key_press(event):
    global game
    if event.keycode == 65:  
        g1.mode = 'top'
    elif event.keycode == 68:  
        g1.mode = 'down'

    elif event.keycode == 32:   
        game = 1


def key_release(event):
    if event.keycode == 65 or event.keycode == 68:
        g1.mode = ''


root.bind('<Key>', key_press)
root.bind('<KeyRelease>', key_release)

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



rT = threading.Thread(target=receving, args=('RecvThread', s))
rT.start()


while 1:
    if game:
        b.move()
    g1.move()
    time.sleep(0.02)
    canv.update()

    
    if '$' in data:
        data_lin = data.split('$')  
        data = data.replace('$', '')
        data_y = float(data_lin[1])
        data_x = 452
        b.x = data_x
        b.y = data_y
        b.vx = -6
        b.vy = -6
        b.kill()
    elif data == '2':
        data = ''
        g1.score += 1
    

root.mainloop()
rT.join()
s.close()