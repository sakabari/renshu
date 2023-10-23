from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///chatdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)

class chat_index(db.Model):
    __tablename__ = 'chat_index'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text)

class chat_conver(db.Model):
    __tablename__ = 'chat_conver'
    id = db.Column(db.Integer, primary_key=True)
    subject = subject = db.Column(db.Text)
    poster = db.Column(db.Text)
    content = db.Column(db.Text)
    img = db.Column(db.Text)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    con = sqlite3.connect('./instance/chatdata.db')
    cur = con.cursor()
    cur.execute("SELECT subject FROM chat_index")
    chatindex = cur.fetchall()
    cur.close()
    con.close()
    return render_template("index.html", chatindex = chatindex, length = len(chatindex))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET':
        return render_template('upload.html')
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        subject = request.form.get('subject_text')
        chatdata = chat_index(subject = subject)
        db.session.add(chatdata)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/uploaded_file')
def uploaded_file():
    return render_template('uploaded_file.html')

@app.route('/chat/<string:subject>', methods=['GET', 'POST'])
def chat(subject):
    if request.method == 'GET':
        pass
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        img_flag = request.form.get('img_presence_or_absence')
        if img_flag  == 'presence':
            file = request.files['img']
            file.save(os.path.join('./static/img', file.filename))
            img = '../static/img/' + file.filename
        else:
            img = 'null'
        content_txt = request.form.get('content')
        poster_txt = request.form.get('poster')
        chatdata_commit = chat_conver(subject = subject, poster = poster_txt, content = content_txt, img = img)
        db.session.add(chatdata_commit)
        db.session.commit()

    con = sqlite3.connect('./instance/chatdata.db')
    cur = con.cursor()
    cur.execute("SELECT subject, poster, content, img FROM chat_conver WHERE subject = ?", (subject,))
    chatdata = cur.fetchall()
    cur.close()
    con.close()
    length = len(chatdata)
    return render_template('chat.html', chatdata = chatdata, length = length)

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)