from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")  # HTML template named 'home.html' is created

@app.route("/contact")
def contact():
    return render_template('contact.html')  # HTML template named 'contact.html' is created

@app.route("/about")
def about():
    return render_template("about.html")  # HTML template named 'about.html' is created

@app.route("/all_character")
def all_character():
    conn = sqlite3.connect("starwar.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Character")
    results = cur.fetchall()
    print(results)
    return render_template("all_character.html", results=results)

@app.route("/Character/<int:id>")
def Character(id):
    conn = sqlite3.connect("starwar.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Character WHERE id=?", (id,))  # Execute SQLite query to retrieve data from "Character" table in the database.
    Character = cur.fetchone()
    print(Character)
    cur.execute("SELECT * FROM Abilities WHERE id=?", (id,))  # Execute SQLite query to retrieve data from "Abilities" table in the database.
    Abilities = cur.fetchone()
    print(Abilities)
    cur.execute("SELECT name FROM The_side WHERE id IN (SELECT aid FROM Character_abilities WHERE cid=?)", (id,))  # Retrieves the names of the sides (e.g., light side or dark side) associated with the character.
    The_side = cur.fetchall()
    print(The_side)

    return render_template("Character.html", Character=Character, Abilities=Abilities, The_side=The_side)

@app.route('/contact', methods=['GET', 'POST'])
def index():  # Function named index to handle the '/contact' route.
    if request.method == 'POST':  # POST is used when submitting data from the server.
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        subject = request.form.get('subject')
        # First/last/subject + name = id where user input data submitted from POST.
        conn = sqlite3.connect('starwar.db')  # Route connects to SQLite (starwar.db).
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (firstname, lastname, subject) VALUES (?, ?, ?)", (firstname, lastname, subject))
        # Execute an SQLite query into the table firstname, lastname, and subject.
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('contact.html')

if   __name__ == "__main__":
    app.run(debug=True)
