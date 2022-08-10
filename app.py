from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime



app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "atestat"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class staff(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    nume = db.Column(db.String(100))
    parola = db.Column(db.String(100))

    def __init__(self, nume, parola):
        self.nume = nume
        self.parola = parola

class mesaje(db.Model):
   _id = db.Column(db.Integer, primary_key = True)
   nume = db.Column(db.String(100))
   email = db.Column(db.String(100))
   subiect = db.Column(db.String(100))
   mesaj = db.Column(db.String(500))

   def __init__(self, nume, email, subiect, mesaj):
       self.nume = nume
       self.email = email
       self.subiect = subiect
       self.mesaj = mesaj


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main', methods=["POST", "GET"])
def main():

    if request.method == 'POST':
        nume = request.form['nameTXT']
        email = request.form['emailTXT']
        subiect = request.form['subjectTXT']
        mesaj = request.form['messageTXT']

        msg = mesaje(nume, email, subiect, mesaj)
        db.session.add(msg)
        db.session.commit()
        flash("Mesajul a fost trimis cu succes!", "succes")

    return render_template('main.html')

@app.route('/login',methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True

        user = request.form["Uname"]
        passwd = request.form["Pass"]
        
        try:
            found_user = staff.query.filter_by(nume = user).first()
        except:
            found_user = staff("","")
    
        adminn = staff.query.filter_by(nume = 'Iuli').first()
        
        if found_user != None and found_user.nume == adminn.nume and passwd == found_user.parola:
            session["user"] = user
            flash(f"Buna, {user}. Te-ai conectat cu succes!", "succes")
            return redirect(url_for("admin"))
        else:
            flash("Parola sau nume incorecte!", "fail")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already logged in!", "fail")
            return redirect(url_for("admin"))
        return render_template('login.html')

@app.route('/admin', methods=["POST", "GET"])
def admin():

    if request.method == 'POST':
        return redirect(url_for("logout"))
    else:
        if "user" in session:
        
            user = session['user']
            return render_template("admin.html", values=mesaje.query.all(), user = user)
        else:
            flash("Nu esti conectat!", "fail")
            return redirect(url_for("login"))

@app.route('/logout')
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Ai fost deconectat, {user}!", "succes")
    session.pop("user", None)
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    
    return render_template('404.html'), 404

if __name__ == "__main__":
    #website_url = 'petruiulian.com'
    #app.config['SERVER_NAME'] = website_url
    db.create_all()
    app.run(debug=True)