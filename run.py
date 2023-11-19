from app import create_app
from flask import Flask
from flask import request

app = Flask(__name__)
 
@app.route("/")
def showHomePage():
    return "This is home page"
 
@app.route("/debug", methods=["POST"])
def debug():
    text = request.form["sample"]
    print(text)
    return "received"

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
    