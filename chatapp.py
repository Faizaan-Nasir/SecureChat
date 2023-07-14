import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QFormLayout, QLineEdit, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
import random
import mysql.connector as sql
#import threading 
import time
#import subprocess
import connection
from connection import con

cur=con.cursor()
app = QApplication([])
app.setWindowIcon(QtGui.QIcon('icon.png'))
window = QWidget()
window.setWindowTitle("SecureChat")
window.setFixedWidth(1400)
window.setFixedHeight(750)
window.setStyleSheet('background:url(background.jpg)')
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

def joinroom(): 
    def main_page():
        ID_label_n.show()
        textor.show()
        roomId.show()
        roomKey.show()
        submit.show()
        instruction.show()
    
    def display():
        cur.execute('select * from {} where reciever="{}";'.format(table_name,roomId.text()))
        l=cur.fetchall()
        y=QLabel('<div style="color:white;font-size:20px;">'+l[-1][2]+'</div>')
        y.setFixedHeight(50)
        y.setStyleSheet('border-radius:10px;background:#005c4b;padding:10px;font-weight:500')
        y.setAlignment(QtCore.Qt.AlignRight)
        chats.addWidget(y)
        chatarea.show()
        
    def sendmes():
        query='insert into {} values("{}","{}","{}")'.format(table_name,code,roomId.text(),message.text())
        li.append(message.text())
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
        
        chats=QVBoxLayout()
        global li
        li=[]
        cur.execute('select * from {} where (reciever="{}" and sender="{}") or (reciever="{}" and sender="{}");'.format(table_name,roomId.text(),code,code,roomId.text()))
        for k in cur.fetchall():
            if k[1]==code:
                x=QLabel('<div style="color:white;font-size:20px;">'+k[2]+'</div>')
                x.setFixedHeight(50)
                x.setStyleSheet('border-radius:10px;background:#202c33;padding:10px;font-weight:500')
                chats.addWidget(x)
            elif k[0]==code:
                y=QLabel('<div style="color:white;font-size:20px;">'+k[2]+'</div>')
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
        
        send=QPushButton('Send',parent=window)
        send.setFixedWidth(170)
        send.setStyleSheet('background:grey;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
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
                    y=QLabel('<div style="color:white;font-size:20px;">'+m[2]+'</div>')
                    y.setFixedHeight(50)
                    y.setStyleSheet('border-radius:10px;background:#202c33;padding:10px;font-weight:500')
                    y.setAlignment(QtCore.Qt.AlignLeft)
                    chats.addWidget(y)
                    chatarea.show()
            QTimer.singleShot(5000,checkForNewMessages)
        checkForNewMessages()
title = QLabel('''
<style>
.hello{
color:white;
}
</style>
<h1 class='hello'> SecureChat </h1>
''', parent=window)
title.setAlignment(QtCore.Qt.AlignCenter)
title.setStyleSheet('font-size:35px;')
title.setFixedWidth(1400)
title.move(0,20)

alert=QLabel('''
<h2 style='color:#F04E4E;'> Please Enter a Valid Room Key </h2>''',parent=window)
alert.move(20,10)
alert.hide()

ID_label_n=QLabel('''
<h2> User ID: '''+code+'''</h2>''',parent=window)
ID_label_n.setAlignment(QtCore.Qt.AlignCenter)
ID_label_n.setFixedWidth(1400)
ID_label_n.setStyleSheet('color:white;font-size:25px;background:transparent')
ID_label_n.move(0,150)

textor=QLabel('''
<h2> Alternatively:</h2''',parent=window)
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
submit.setStyleSheet('font-size:25px; font-weight:600; background:light grey; color:white; border-radius:10px;padding:10px')
submit.setFixedHeight(50)
submit.move(965,350)
submit.clicked.connect(joinroom)

instruction=QLabel('''
<style>
h2{
font-size:30px;
}
</style>
<h2> Instructions: </h2>
Ask your friends to install this app and send the room code and key that they see on their app.
You <br> may enter this in your device and continue chatting privately. The messages you send are not end<br>
to end encrypted, please do not share your key with anyone else. Your key is '''+keyn+'''.''',parent=window)
instruction.setStyleSheet('color:white;font-size:25px;font-weight:500;background:transparent')
instruction.setFixedWidth(1230)
instruction.move(85,500)

window.show()
sys.exit(app.exec())