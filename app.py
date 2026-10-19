
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "practice-secret-key"

USERNAME = "Rafay"
PASSWORD = "1234"
balance = 5000


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        if name == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect("/menu")

        return "Wrong name or password!"

    return render_template("login.html")


@app.route("/menu")
def menu():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("menu.html")


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    global balance

    if not session.get("logged_in"):
        return redirect("/")

    message = ""

    if request.method == "POST":
        name = request.form["name"]
        amount = float(request.form["amount"])

        if amount <= 0:
            message = "Enter a valid amount!"
        elif amount > balance:
            message = "Insufficient balance!"
        else:
            balance -= amount
            message = f"${amount:g} sent to {name}!"

    return render_template("transfer.html", message=message)


@app.route("/info")
def info():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("info.html", name=USERNAME)


@app.route("/balance")
def check_balance():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("balance.html", balance=balance)


if __name__ == "__main__":
    app.run(debug=True)
