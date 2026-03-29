from flask import Flask

app = Flask(__name__)

from views import *

if __name__ == "__main__":
    app.run()

''' 
@app.route("/get", methods=["GET","POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)


def get_Chat_response(text):
''' 
