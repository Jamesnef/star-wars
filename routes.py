from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("home.html")

@app.route("/contact")
def contact():
    conn = sqlite3.connect('starwar')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    entries = cursor.fetchall()
    conn.close()
    return render_template('contact.html', entries)

@app.route('/add_entry', methods=['POST'])
def add_entry(): #def add entry = save entry
    if request.method == 'POST':  #check if method = post or ?
        content = request.form['content']  #content = databse / rqf = data submit in form from box
        conn = sqlite3.connect('starwar.db')  # sqlite connect database
        cursor = conn.cursor()  #worker ahhhhhhhhh *connection with db*
        cursor.execute("INSERT INTO entries (content) VALUES (?)", (content,)) 
        conn.commit()  #save permit trong db / ko có dòng này là save temp
        conn.close()  #close connection
    return redirect('/')  
    

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




if __name__ == "__main__":
    app.run(debug=True)