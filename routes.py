from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("home.html")

@app.route("/contact")
def contact():
    return render_template('contact.html')

    

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/all_character")
def all_character():
    conn=sqlite3.connect("starwar.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Character")
    results = cur.fetchall()
    print(results)
    return render_template("all_character.html", results=results)


@app.route("/Character/<int:id>")
def Character(id):
    conn=sqlite3.connect("starwar.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM Character WHERE id=?",(id,))
    Character = cur.fetchone()
    print(Character)
    cur.execute("SELECT * FROM Abilities WHERE id=?",(id,))
    Abilities = cur.fetchone()
    print(Abilities)
    cur.execute("SELECT name FROM The_side WHERE id in( SELECT aid FROM Character_abilities WHERE cid=?)",(id,))
    The_side = cur.fetchall()
    print(The_side)
    
    return render_template("Character.html",Character=Character, Abilities=Abilities, The_side=The_side )

@app.route('/contact', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        subject = request.form.get('subject')
        conn = sqlite3.connect('starwar.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (firstname, lastname, subject) VALUES (?, ?, ?)", (firstname, lastname, subject))
        conn.commit()
        conn.close()
        return redirect ('/')
    return render_template('contact.html')




if __name__ == "__main__":
    app.run(debug=True)