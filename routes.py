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
    # Connect to the SQLite database.
    conn = sqlite3.connect("starwar.db")
    cur = conn.cursor()
    # Execute an SQL query to retrieve all character data.
    cur.execute("SELECT * FROM Character")
    results = cur.fetchall()
    print(results)
    return render_template("all_character.html", results=results)


@app.route("/Character/<int:id>")
def Character(id):
    conn = sqlite3.connect("starwar.db")
    cur = conn.cursor()
    # Check if the character with the given ID exists
    cur.execute("SELECT * FROM Character WHERE id=?", (id,))
    Character = cur.fetchone()
    if Character is None:
        abort(404)
    # If the character exists, fetch other related data
    cur.execute("SELECT * FROM Abilities WHERE id=?", (id,))
    Abilities = cur.fetchone()
    print(Abilities)
    # Executing the query from SQLITE
    cur.execute(
        "SELECT name FROM The_side WHERE id IN \
        (SELECT aid FROM Character_abilities WHERE cid=?)", (id,))
    The_side = cur.fetchall()
    print(The_side)
    # Executing the query from SQLITE
    cur.execute("SELECT photo FROM Character WHERE id=?", (id,))
    photo = cur.fetchone()
    print(photo)
    # Executing the query from SQLITE
    cur.execute("SELECT long_description FROM Character WHERE id=?", (id,))
    long_description = cur.fetchone()
    print(long_description)

    return render_template("Character.html", Character=Character, Abilities=Abilities, 
                           The_side=The_side, photo=photo, long_description=long_description)

@app.route('/contact', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('firstname')  # Variable "name"
        contact = request.form.get('lastname')  # Variable "contact"
        subject = request.form.get('subject')  # Variable "subject"
        # Connect to the SQLite database
        conn = sqlite3.connect('starwar.db')
        cursor = conn.cursor()
        # Insert the user input into the database from the website
        cursor.execute("INSERT INTO entries (name, contact, subject) VALUES (?, ?, ?)", (name, contact, subject))
        # Commit the changes and close the database connection
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
