from flask import Flask, render_template, request, session,redirect,url_for
from flask_socketio import join_room,leave_room,send,SocketIO
import random
from string import ascii_uppercase

app=Flask(__name__)
app.config['SECRET_KEY']="erjhhercb"
socketio=SocketIO(app)

rooms={}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code+=random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


@app.route("/",methods=["GET","POST"])
def home():
    session.clear()
    if request.method=="POST":
        name=request.form.get("name")
        code=request.form.get("code")
        join=request.form.get("join",False)         #form is a dictionary, so if join is not present then it will be false
        create=request.form.get("create",False)     #since join and create have empty values

        if not name:
            return render_template("home.html",error="Please enter a name", code = code, name = name) #post req re-renders page every time hence remind it
        
        if join!=False and not code:
            return render_template("home.html",error="Please enter a room code",code = code, name = name)
        
        room = code
        if create!=False:
            room=generate_unique_code(4)
            rooms[room]={"members":0,"messages":[]}
        elif code not in rooms:
            return render_template("home.html",error="Room does not exist")
        
        session["room"]=room   #we dont use auth, so we are storing room and name in temp session
        session["name"]=name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    return render_template("room.html")


if __name__=="__main__":
    socketio.run(app,debug=True)

