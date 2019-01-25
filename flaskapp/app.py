from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def hello():
    #return "Hello, Flask!"
    values = {"val1": 100, "val2": 200}
    return render_template("index.html", values=values)

if __name__ == "__main__":
    app.run()
