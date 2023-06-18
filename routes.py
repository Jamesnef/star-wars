from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("home.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/all_character")
def all_pizzas():
    conn=sqlite3.connect("starwar")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Character")
    results = cur.fetchall()
    print(results)
    return render_template("all_character.html", results=results)


@app.route("/Character/<int:id>")
def pizza(id):
    conn=sqlite3.connect("pizza1.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM  WHERE id=?",(id,))
    pizza = cur.fetchone()
    print(pizza)
    cur.execute("SELECT * FROM BASE WHERE id=?",(id,))
    base = cur.fetchone()
    print(base)
    cur.execute("SELECT name FROM Topping WHERE id in( SELECT tid FROM PizzaTopping WHERE pid=?)",(id,))
    topping = cur.fetchall()
    print(topping)
    
    return render_template("pizza.html",pizza=pizza, base=base, topping=topping )




if __name__ == "__main__":
    app.run(debug=True)