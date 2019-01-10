from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<html><body><h1>sample</h1></body></html>'

if __name__ == '__main__':
    # if this program works on Vagrant, 
    # set ip address 0.0.0.0 or Vagrant default ip address.
    app.run("192.168.33.10", debug=True)