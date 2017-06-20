from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True

form = """
<!doctype html>
<form action="/hello" method="GET">
    <label for="name">What is your name?</label>
    <input type="text" name="name" id="name">
    <input type="submit">
</form>
"""

@app.route("/")
def index():
    return form

@app.route("/hello")
def hello():
    name = request.args.get('name')

    return name

if __name__ == "__main__":
    app.run()