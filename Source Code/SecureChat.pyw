# This is only the source code of the executable and alot of the sensitive information has been populated and hence hidden with placeholder

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFormLayout, QLineEdit, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
import random
import mysql.connector as sql
import time

con=sql.connect(host='SQL HOSTING SERVER',user='THE USERNAME',password='THE PASSWORD',database='THE DATABASE')

cur=con.cursor()
app = QApplication([])
app.setWindowIcon(QtGui.QIcon('./src/icon.png'))
window = QWidget()
window.setWindowTitle("SecureChat")
window.setFixedWidth(1400)
window.setFixedHeight(750)
window.setStyleSheet('background:url("./src/blurple.png") no-repeat fixed center;')
keyn=''
for i in range(6):
    a=random.randint(0,25)
    keyn+=chr(a+65)
    
newkey=''
for i in range(7):
    j=random.randint(0,25)
    newkey+=chr(j+65)
try:
    code=open('key.txt','r').read()
except:
    newfile=open('key.txt','x')
    newfile.close()
    key=open('key.txt','w')
    key.write(newkey)
    code=newkey
    key.close()
    print(code)
global send
def joinroom(): 
    def main_page():
        ID_label_n.show()
        textor.show()
        roomId.show()
        roomKey.show()
        submit.show()
        instruction.show()
        theme.show()
    
    def display():
        cur.execute('select * from {} where reciever="{}";'.format(table_name,roomId.text()))
        l=cur.fetchall()
        s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        s2='SUBSTITUTION KEY'
        decrypt=''
        for j in l[-1][2]:
            if j.isalpha():
                x=s2.index(j)
                decrypt+=s1[x]
            else:
                decrypt+=j
        y=QLabel('<div style="color:white;font-size:20px;width:780px">'+decrypt+'</div>')
        y.setWordWrap(True)
        y.setFixedHeight(50)
         
        y.setStyleSheet('border-radius:10px;background:#005c4b;padding:10px;font-weight:500')
        y.setAlignment(QtCore.Qt.AlignRight)
        chats.addWidget(y)
        chatarea.show()
        
    def sendmes():
        s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        s2='SUBSTITUTION KEY'
        text=message.text()
        encrypt=''
        for i in text:
            if i.isalpha():
                x=s1.index(i)
                encrypt+=s2[x]
            else:
                encrypt+=i
        query='insert into {} values("{}","{}","{}")'.format(table_name,code,roomId.text(),encrypt)
        li.append(encrypt)
        cur.execute(query)
        con.commit()
        display()
    
    def gobackF():
        chatarea.hide()
        ID_label.hide()
        key_label.hide()
        message.hide()
        send.hide()
        goback.hide()
        delete.hide()
        main_page()
        gobackt=True
        theme.show()
        
    def deleteF():
        cur.execute('delete from {} where (reciever="{}" and sender="{}") or (reciever="{}" and sender="{}");'.format(table_name,roomId.text(),code,code,roomId.text()))
        gobackF()
        con.commit()
    
    room_key=roomKey.text()
    if room_key in ['Enter Room Key',''] or len(room_key)!=6:
        alert.show()
    else:
        table_name=roomKey.text()
        try:
            cur.execute("select * from {};".format(table_name))
            cur.fetchall()
        except:
            cur.execute("create table {} (sender varchar(20),reciever varchar(20),message varchar(500))".format(table_name))
        ID_label_n.hide()
        textor.hide()
        roomId.hide()
        roomKey.hide()
        submit.hide()
        alert.hide()
        instruction.hide()
        global message
        box=QHBoxLayout()
        ID_label=QLabel('''
    <h2> User ID: '''+roomId.text()+'''</h2>''',parent=window)
        ID_label.setStyleSheet('color:white;font-size:25px;background:transparent')
        ID_label.move(239,150)
        ID_label.show()
        key_label=QLabel('''
    <h2> Room Key: '''+room_key+'''</h2>''',parent=window)
        key_label.setStyleSheet('color:white;font-size:25px;background:transparent')
        key_label.move(785,150)
        key_label.show()
        
        chatarea=QScrollArea(parent=window)
        chatarea.move(300,250)
        chatarea.resize(800,300)
        chatarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        chatarea.setWidgetResizable(True)
        chatarea.setStyleSheet('border:none;background:transparent;')
        theme.hide()
        
        chats=QVBoxLayout()
        global li
        li=[]
        cur.execute('select * from {} where (reciever="{}" and sender="{}") or (reciever="{}" and sender="{}");'.format(table_name,roomId.text(),code,code,roomId.text()))
        s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        s2='SUBSTITUTION KEY'
        for k in cur.fetchall():
            if k[1]==code:
                decrypt=''
                for j in k[2]:
                    if j.isalpha():
                        x=s2.index(j)
                        decrypt+=s1[x]
                    else:
                        decrypt+=j
                x=QLabel('<div style="color:white;font-size:20px;">'+decrypt+'</div>')
                x.setWordWrap(True)
                x.setFixedHeight(50)
                x.setStyleSheet('border-radius:10px;background:#202c33;padding:10px;font-weight:500')
                chats.addWidget(x)
            elif k[0]==code:
                decrypt=''
                for j in k[2]:
                    if j.isalpha():
                        x=s2.index(j)
                        decrypt+=s1[x]
                    else:
                        decrypt+=j
                y=QLabel('<div style="color:white;font-size:20px;">'+decrypt+'</div>')
                y.setWordWrap(True)
                y.setFixedHeight(50)
                y.setStyleSheet('border-radius:10px;background:#005c4b;padding:10px;font-weight:500')
                y.setAlignment(QtCore.Qt.AlignRight)
                chats.addWidget(y)
            li.append(k[2])
        new=QWidget()
        new.setLayout(chats)
        chatarea.setWidget(new)
        chatarea.show()
        
        message=QLineEdit('Enter your message here...',parent=window)
        message.setFixedWidth(600)
        message.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
        message.move(311,590)
        message.show()
        
        global send
        send=QPushButton('Send',parent=window)
        send.setFixedWidth(170)
        send.setStyleSheet('background:{};border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500'.format(color))
        send.move(919,590)
        send.clicked.connect(sendmes)
        send.show()

        goback=QPushButton('Go Back',parent=window)
        goback.setFixedWidth(384)
        goback.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
        goback.move(705,670)
        goback.clicked.connect(gobackF)
        goback.show()
        
        delete=QPushButton('Delete Conversation',parent=window)    
        delete.setFixedWidth(384)
        delete.setStyleSheet('background:#F04E4E;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
        delete.move(311,670)
        delete.clicked.connect(deleteF)
        delete.show()
        
        def checkForNewMessages():
            con.commit()
            cur.execute('select * from {} where (reciever="{}" and sender="{}") or (reciever="{}" and sender="{}");'.format(table_name,roomId.text(),code,code,roomId.text()))
            for m in cur.fetchall():
                if m[2] not in li:
                    li.append(m[2])
                    s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                    s2='SUBSTITUTION KEY'
                    decrypt=''
                    for j in m[2]:
                        if j.isalpha():
                            x=s2.index(j)
                            decrypt+=s1[x]
                        else:
                            decrypt+=j
                    y=QLabel('<div style="color:white;font-size:20px;width:550px">'+decrypt+'</div>')
                    y.setFixedHeight(50)
                    y.setWordWrap(True)
                    y.setStyleSheet('border-radius:10px;background:#202c33;padding:10px;font-weight:500')
                    y.setAlignment(QtCore.Qt.AlignLeft)
                    chats.addWidget(y)
                    chatarea.show()
            QTimer.singleShot(5000,checkForNewMessages)
        checkForNewMessages()
color='#66588a'
def changetheme():
    def theme3Change():
        global color
        window.setStyleSheet('background:url("./src/blurple.png") no-repeat fixed center;')
        submit.setStyleSheet('font-size:25px; font-weight:600; background:#66588a; color:white; border-radius:10px;padding:10px')
        back.setStyleSheet('font-size:25px; font-weight:600; background:#66588a; color:white; border-radius:10px;padding:10px')
        theme.setStyleSheet('font-size:25px; font-weight:600; background:#66588a; color:white; border-radius:10px;padding:10px')
        color='#66588a'
    def theme1Change():
        global color
        window.setStyleSheet('background:url("./src/purple.png") no-repeat fixed center;')        
        submit.setStyleSheet('font-size:25px; font-weight:600; background:#aa6c68; color:white; border-radius:10px;padding:10px')
        back.setStyleSheet('font-size:25px; font-weight:600; background:#aa6c68; color:white; border-radius:10px;padding:10px')
        theme.setStyleSheet('font-size:25px; font-weight:600; background:#aa6c68; color:white; border-radius:10px;padding:10px')
        color='#aa6c68'
    def theme2Change():
        global color
        window.setStyleSheet('background:url("./src/orange.png") no-repeat fixed center;')
        submit.setStyleSheet('font-size:25px; font-weight:600; background:#c17b60; color:white; border-radius:10px; padding:10px')
        back.setStyleSheet('font-size:25px; font-weight:600; background:#c17b60; color:white; border-radius:10px; padding:10px')
        theme.setStyleSheet('font-size:25px; font-weight:600; background:#c17b60; color:white; border-radius:10px; padding:10px')
        color='#c17b60'
    def backtheme():
        changeTheme.hide()
        theme1.hide()
        theme2.hide()
        theme3.hide()
        back.hide()
        theme.show()
        ID_label_n.show()
        textor.show()
        roomId.show()
        roomKey.show()
        submit.show()
        instruction.show()
    ID_label_n.hide()
    textor.hide()
    roomId.hide()
    roomKey.hide()
    submit.hide()
    alert.hide()
    instruction.hide()
    theme.hide()
    changeTheme=QLabel('''<h2 style="text-align:center">Change Theme</h2>''',parent=window)
    changeTheme.setAlignment(QtCore.Qt.AlignCenter)
    changeTheme.setStyleSheet('font-size:25px;color:white;background:transparent')
    changeTheme.setFixedWidth(1400)
    changeTheme.move(0,120)
    changeTheme.show()
    theme3=QPushButton('BLURPLE',parent=window)
    theme3.setFixedWidth(290)
    theme3.setFixedHeight(150)
    theme3.move(550,550)
    theme3.setStyleSheet('font-weight:600;font-size:23px;background:url("./src/blurple.png");border: 5px solid white;border-radius:10px')
    theme3.show()
    theme3.clicked.connect(theme3Change)
    theme1=QPushButton('PURPLE',parent=window)
    theme1.setFixedWidth(290)
    theme1.setFixedHeight(150)
    theme1.setStyleSheet('font-weight:600;font-size:23px;background:url("./src/purple.png");border: 5px solid white;border-radius:10px')
    theme1.move(550,200)
    theme1.show()
    theme1.clicked.connect(theme1Change)
    theme2=QPushButton('ORANGE',parent=window)
    theme2.setFixedWidth(290)
    theme2.setFixedHeight(150)
    theme2.setStyleSheet('font-weight:600;font-size:23px;background:url("./src/orange.png");border: 5px solid white;border-radius:10px')
    theme2.move(550,375)
    theme2.show()
    theme2.clicked.connect(theme2Change)
    back=QPushButton('Back',parent=window)
    back.setFixedWidth(150)
    back.setStyleSheet('font-size:25px; font-weight:600; background:{}; color:white; border-radius:10px;padding:10px'.format(color))
    back.setFixedHeight(50)
    back.move(1210,40)
    back.clicked.connect(backtheme)
    back.show()
title = QLabel('''<h1>SecureChat</h1>''', parent=window)
title.setFixedWidth(1400)
title.setAlignment(QtCore.Qt.AlignCenter)
title.setStyleSheet('font-size:35px;color:white;background:transparent;')
title.move(0,20)

alert=QLabel('''
<h2 style='color:#F04E4E;'> Please Enter a Valid Room Key </h2>''',parent=window)
alert.setStyleSheet('background:transparent')
alert.move(20,10)
alert.hide()

ID_label_n=QLabel('''
<h2> User ID: '''+code+'''</h2>''',parent=window)
ID_label_n.setAlignment(QtCore.Qt.AlignCenter)
ID_label_n.setFixedWidth(1400)
ID_label_n.setStyleSheet('color:white;font-size:25px;background:transparent')
ID_label_n.move(0,150)

textor=QLabel('''
<h2> Create/Enter Room:</h2>''',parent=window)
textor.setStyleSheet('color:white; font-size:30px;background:transparent')
textor.move(84,240)

roomId=QLineEdit('Enter Reciever ID',parent=window)
roomId.setStyleSheet('border:none; background: white; border-radius:10px;font-size:25px;font-weight:500; padding:10px;border:none')
roomId.setFixedHeight(50)
roomId.setFixedWidth(400)
roomId.move(84,350)
roomKey=QLineEdit('Enter Room Key',parent=window)
roomKey.setStyleSheet('border:none; background: white; border-radius:10px;font-size:25px;font-weight:500; padding:10px;border:none')
roomKey.setFixedHeight(50)
roomKey.setFixedWidth(400)
roomKey.move(520,350)

submit=QPushButton('Submit',parent=window)
submit.setFixedWidth(350)
submit.setStyleSheet('font-size:25px; font-weight:600; background:#66588a; color:white; border-radius:10px;padding:10px')
submit.setFixedHeight(50)
submit.move(965,350)
submit.clicked.connect(joinroom)

theme=QPushButton('Theme',parent=window)
theme.setFixedWidth(150)
theme.setStyleSheet('font-size:25px; font-weight:600; background:#66588a; color:white; border-radius:10px;padding:10px')
theme.setFixedHeight(50)
theme.move(1210,40)
theme.clicked.connect(changetheme)

instruction=QLabel('''
<style>
h2{
font-size:30px;
}
</style>
<h2> Instructions: </h2>
Ask your friends to install this app and send the room code and key that they see on their app.
You <br> may enter this in your device and continue chatting privately. The messages you send are encrypted,<br>
please do not share your key with anyone else. Your key is '''+keyn+'''.''',parent=window)
instruction.setStyleSheet('color:white;font-size:25px;font-weight:500;background:transparent')
instruction.setFixedWidth(1230)
instruction.move(85,500)

window.show()
sys.exit(app.exec())