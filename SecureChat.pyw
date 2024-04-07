import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
import random
import mysql.connector as sql
import math
import random
import keyboard

try:
    con=sql.connect(charset="utf8mb4",host='MORPHED',port=21134,user='MORPHED',password='MORPHED',database="MORPHED")
except Exception as errors:
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon('./src/icon.png'))
    window = QWidget()
    window.setWindowTitle("SecureChat")
    window.setFixedWidth(1400)
    window.setFixedHeight(750)
    window.setStyleSheet('background:url("./src/blurple.png") no-repeat fixed center;')
    ID_label=QLabel('''
    <h2 align='center'>Oops... we could not connect to our server.<br>
    Please create an issue on GitHub with your log file attached.</h2>''',parent=window)
    ID_label.setStyleSheet('color:white;font-size:25px;background:transparent')
    ID_label.move(125,300)
    ID_label.show()
    window.show()
    with open('log.txt','w') as logfile:
        logfile.write(str(errors))
    couldnotconnect=True
else:
    couldnotconnect=False
    cur=con.cursor()
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon('./src/icon.png'))
    window = QWidget()
    window.setWindowTitle("SecureChat")
    window.setFixedWidth(1400)
    window.setFixedHeight(750)
    window.setStyleSheet('background:url("./src/blurple.png") no-repeat fixed center;')
    a=random.randint(100000,999999)
    keyn='A'+str(a)
    
    global send
    def joinroom():
        global inside
        def main_page():
            ID_label_n.show()
            textor.show()
            roomId.show()
            roomKey.show()
            submit.show()
            instruction.show()
            theme.show()
        
        def display(insertkey):
            cur.execute('''select * from {} where reciever='{}';'''.format(table_name,roomId.text()))
            l=cur.fetchall()
            s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            random.seed(int(insertkey[1:]))
            s2=''.join(random.sample(s1,len(s1)))
            decrypt=''
            for j in l[-1][2]:
                if j.isalpha():
                    x=s2.index(j)
                    decrypt+=s1[x]
                else:
                    decrypt+=j
            y=QLabel('<p style="color:white;font-size:20px;width:780px">'+decrypt+'</p>')
            y.setStyleSheet('border-radius:10px;background:#005c4b;padding:10px;font-weight:500')
            y.setAlignment(QtCore.Qt.AlignRight)
            y.setWordWrap(True)
            count=math.ceil(len(decrypt)/60)
            y.setFixedHeight(30*count+20)
            chats.addWidget(y)
            chatarea.show()
            
        def sendmes(insertkey):
            s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            random.seed(int(insertkey[1:]))
            s2=''.join(random.sample(s1,len(s1)))
            alert1=QLabel('''<h2 style='color:#F04E4E;'> Empty Message!! </h2>''',parent=window)
            alert1.setStyleSheet('background:transparent')
            alert1.move(20,10)
            text=message.text()
            if text.strip()=='':
                alert1.show()
                def hidealert():
                    alert1.hide()
                QTimer.singleShot(3000,hidealert)
            else:
                encrypt=''
                for i in text:
                    if i.isalpha():
                        x=s1.index(i)
                        encrypt+=s2[x]
                    else:
                        encrypt+=i
                cur.execute('select * from {};'.format(table_name))
                data=cur.fetchall()
                try:
                    currval=data[-1][-1]
                except:
                    currval=1
                query='''insert into {} values('{}','{}','{}',{})'''.format(table_name,code,roomId.text(),encrypt,currval+1)
                li.append(encrypt)
                cur.execute(query)
                con.commit()
                display(insertkey)
                message.clear()
        
        def gobackF():
            global inside
            chatarea.hide()
            ID_label.hide()
            key_label.hide()
            message.hide()
            send.hide()
            goback.hide()
            delete.hide()
            main_page()
            gobackt=True
            inside=False
            theme.show()
            
        def deleteF():
            cur.execute('''delete from {} where (reciever='{}' and sender='{}') or (reciever='{}' and sender='{}');'''.format(table_name,roomId.text(),code,code,roomId.text()))
            gobackF()
            con.commit()
        
        room_key=roomKey.text()
        if room_key in ['Enter Room Key',''] or len(room_key)!=7 or not(room_key[0].isalpha()):
            alert.show()
        else:
            table_name=roomKey.text()
            try:
                cur.execute("select * from {};".format(table_name))
                cur.fetchall()
            except:
                cur.execute("create table {} (sender varchar(20),reciever varchar(20),message varchar(1000),msgid int primary key)".format(table_name))
            ID_label_n.hide()
            textor.hide()
            roomId.hide()
            roomKey.hide()
            submit.hide()
            alert.hide()
            instruction.hide()
            global message
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
            chatarea.setStyleSheet('border:none;background:transparent;')
            chatarea.setWidgetResizable(True)
            theme.hide()
            
            chats=QVBoxLayout(window)
            global li
            li=[]
            cur.execute('''select * from {} where (reciever='{}' and sender='{}') or (reciever='{}' and sender='{}');'''.format(table_name,roomId.text(),code,code,roomId.text()))
            s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            random.seed(int(room_key[1:]))
            s2=''.join(random.sample(s1,len(s1)))
            for k in cur.fetchall():
                if k[1]==code:
                    decrypt=''
                    for j in k[2]:
                        if j.isalpha():
                            x=s2.index(j)
                            decrypt+=s1[x]
                        else:
                            decrypt+=j
                    x=QLabel('<p style="color:white;font-size:20px;">'+decrypt+'</p>')
                    x.setWordWrap(True)
                    count=math.ceil(len(decrypt)/60)
                    x.setFixedHeight(30*count+20)
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
                    y=QLabel('<p style="color:white;font-size:20px;">'+decrypt+'</p>')
                    y.setWordWrap(True)
                    count=math.ceil(len(decrypt)/60)
                    y.setFixedHeight(30*count+20)
                    y.setStyleSheet('border-radius:10px;background:#005c4b;padding:10px;font-weight:500')
                    y.setAlignment(QtCore.Qt.AlignRight)
                    chats.addWidget(y)
                li.append(k[2])
            new=QWidget()
            new.setLayout(chats)
            chatarea.setWidget(new)
            chatarea.show()
            
            message=QLineEdit(parent=window)
            message.setFixedWidth(600)
            message.setStyleSheet('font-size:25px;border:none;background:white;border-radius:10px;padding:10px')
            message.move(311,590)
            message.show()
            message.setPlaceholderText('Enter your message here')
            
            global send
            send=QPushButton('Send',parent=window)
            send.setFixedWidth(170)
            send.setStyleSheet('background:{};border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500'.format(color))
            send.move(919,590)
            send.clicked.connect(lambda: sendmes(room_key))
            send.show()
            inside=True
            
            def sendenter():
                if keyboard.is_pressed('enter'):
                    sendmes(room_key)
                if inside:
                    QTimer.singleShot(50,sendenter)
            sendenter()
            
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
            
            def checkForNewMessages(insertkey):
                con.commit()
                cur.execute('''select * from {} where (reciever='{}' and sender='{}') or (reciever='{}' and sender='{}');'''.format(table_name,roomId.text(),code,code,roomId.text()))
                for m in cur.fetchall():
                    if m[2] not in li:
                        li.append(m[2])
                        s1='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                        random.seed(int(insertkey[1:]))
                        s2=''.join(random.sample(s1,len(s1)))
                        decrypt=''
                        for j in m[2]:
                            if j.isalpha():
                                x=s2.index(j)
                                decrypt+=s1[x]
                            else:
                                decrypt+=j
                        y=QLabel('<p style="color:white;font-size:20px;width:550px">'+decrypt+'</p>')
                        y.setWordWrap(True)
                        count=math.ceil(len(decrypt)/60)
                        y.setFixedHeight(30*count+20)
                        y.setStyleSheet('border-radius:10px;background:#202c33;padding:10px;font-weight:500')
                        y.setAlignment(QtCore.Qt.AlignLeft)
                        chats.addWidget(y)
                        chatarea.show()
                QTimer.singleShot(5000,lambda:checkForNewMessages(room_key))
            checkForNewMessages(room_key)
            
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

    textor=QLabel('''
    <h2> Create/Enter Room:</h2>''',parent=window)
    textor.setStyleSheet('color:white; font-size:30px;background:transparent')
    textor.move(84,240)

    roomId=QLineEdit(parent=window)
    roomId.setPlaceholderText('Enter Reciever ID')
    roomId.setStyleSheet('border:none; background: white; border-radius:10px;font-size:25px;font-weight:500; padding:10px;border:none')
    roomId.setFixedHeight(50)
    roomId.setFixedWidth(400)
    roomId.move(84,350)
    roomKey=QLineEdit(parent=window)
    roomKey.setPlaceholderText('Enter Room Key')
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
    font-size: 30px;
    }
    </style>
    <h2> Instructions: </h2>
    Ask your friends to install this app and send the room code and key that they see on their app.
    You <br> may enter this in your device and continue chatting privately. The messages you send are encrypted,<br>
    please do not share your key with anyone else. Your key is '''+keyn+'''.''',parent=window)
    instruction.setStyleSheet('color:white;font-size:25px;font-weight:500;background:transparent')
    instruction.setFixedWidth(1230)
    instruction.move(85,500)
    def newcode():
        with open('key.txt','w') as file:
            file.write(newID.text())
        global code
        code=newID.text()
        idwindow.hide()
        ID_label_n=QLabel('''<h2> User ID: '''+code+'''</h2>''',parent=window)
        ID_label_n.setAlignment(QtCore.Qt.AlignCenter)
        ID_label_n.setFixedWidth(1400)
        ID_label_n.setStyleSheet('color:white;font-size:25px;background:transparent')
        ID_label_n.move(0,150)
        window.show()
    
    idwindow = QWidget()
    idwindow.setWindowTitle("SecureChat")
    idwindow.setFixedWidth(1000)
    idwindow.setFixedHeight(550)
    idwindow.setStyleSheet('background:url("./src/blurple.png") no-repeat fixed center;')
    newID_label=QLabel('''
    <h2 align='center'>Welcome to SecureChat!<br> To continue, please provide your name or alias.<h2>''',parent=idwindow)
    newID_label.setStyleSheet('color:white;font-size:25px;background:transparent')
    newID_label.move(45,150)
    newID=QLineEdit(parent=idwindow)
    newID.setPlaceholderText('Enter your name')
    newID.setStyleSheet('border:none; background: white; border-radius:10px;font-size:25px;font-weight:500; padding:10px;border:none')
    newID.setFixedHeight(50)
    newID.setFixedWidth(400)
    newID.move(200,300)
    subnewid=QPushButton('Submit',parent=idwindow)
    subnewid.setFixedWidth(170)
    subnewid.setStyleSheet('background:#66588a;border-radius:10px;font-size:25px;padding:10px;color:white;font-weight:500')
    subnewid.move(620,300)
    subnewid.clicked.connect(newcode)
            
    try:
        code=open('key.txt','r').read()
        ID_label_n=QLabel('''<h2> User ID: '''+code+'''</h2>''',parent=window)
        ID_label_n.setAlignment(QtCore.Qt.AlignCenter)
        ID_label_n.setFixedWidth(1400)
        ID_label_n.setStyleSheet('color:white;font-size:25px;background:transparent')
        ID_label_n.move(0,150)
        window.show()
    except:
        idwindow.show()
        newID_label.show()
        subnewid.show()
        code=''
appexe=app.exec()
if not(couldnotconnect):
    con.close()
sys.exit(appexe)
