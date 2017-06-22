from flask import Flask, request, redirect

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

lc_form = """
<!doctype html>
<html>
<body>
    <style>
        br {margin-bottom: 20px;}
    </style>

    <form method='POST'>
        <label>type=text
            <input name="user-name" type="text" />
        </label>
        <br>
        <label>type=password
            <input name="user-password" type="password" />
        </label>
        <br>
        <label>type=email
            <input name="user-email" type="email" />
        </label>
        <br>
        <input name="shopping-cart-id" value="0129384" type="hidden" />
        <br>
        <label>Ketchup
            <input type="checkbox" name="cb1" value="first-cb" />
        </label>
        <br>
        <label>Mustard
            <input type="checkbox" name="cb2" value="second-cb" />
        </label>
        <br>
        <label>Small
            <input type="radio" name="coffee-size" value="sm" />
        </label>
        <label>Medium
            <input type="radio" name="coffee-size" value="med" />
        </label>
        <label>Large
            <input type="radio" name="coffee-size" value="lg" />
        </label>
        <br>
        <label>Your life story
            <textarea name="life-story"></textarea>
        </label>
        <br>
        <label>LaunchCode Hub
            <select name="lc-hub">
                <option value="kc">Kansas City</option>
                <option value="mia">Miami</option>
                <option value="ri">Providence</option>
                <option value="sea">Seattle</option>
                <option value="pdx">Portland</option>
            </select>
        </label>
        <br>
        <input type="submit" />
    </form>
</body>
</html>
"""

time_form = """
<style>
    .error {{ color: red; }}
</style>
<h1></h1>
<form action="" method="POST">
    <label>Hours (24-hour format):
        <input name="hours" type="text" value="{hours}" />
    </label>
    <p class="error">{hours_error}</p>

    <label>Minutes:
        <input name="minutes" type="text" value="{minutes}" />
    </label>
    <p class="error">{minutes_error}</p>
    <input type="submit" value="Validate" />
</form>
"""

@app.route("/")
def index():
    return form

@app.route("/hello")
def hello():
    name = request.args.get('name')
    return name

@app.route("/form-inputs")
def form_inputs():
    return lc_form

@app.route("/form-inputs", methods=["POST"])
def print_form_values():
    response = ""
    for field in request.form.keys():
        response += "<b>{key}</b>: {value}<br>".format(key=field, value=request.form[field])
    return response


@app.route("/validate-time")
def display_time_form():
    return time_form.format(hours="",
                            hours_error="",
                            minutes="",
                            minutes_error="")

def is_integer(num_string):
    try:
        int(num_string)
        return True
    except ValueError:
        return False

@app.route("/validate-time", methods=["POST"])
def validate_time():
    
    hours = request.form["hours"]
    minutes = request.form["minutes"]

    hours_error = ""
    minutes_error = ""

    # check if given integer values
    if not is_integer(hours):
        hours_error = "Not a valid integer."
        hours = "" # clear it out to redisplay form without it
    else:
        hours = int(hours)
        if hours > 23 or hours < 0:
            hours_error = "Hours value out of range (0-23)."
            hours = "" # clear it out to redisplay form without it

    if not is_integer(minutes):
        minutes_error = "Not a valid integer."
        minutes = "" # clear it out to redisplay form without it
        
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = "Minutes value out of range (0-59)."
            minutes = "" # clear it out to redisplay form without it

    if not minutes_error and not hours_error: # empty string is truthy 
        time = str(hours) + ":" + str(minutes)
        return redirect("valid-time?time={0}".format(time))
    else:
        return time_form.format(hours=hours,
                        hours_error=hours_error,
                        minutes=minutes,
                        minutes_error=minutes_error)

@app.route("/valid-time")
def valid_time():
    time = request.args.get("time")
    return "<h1>You submited {0}. Thanks for submitting a valid time!</h1>".format(time)


if __name__ == "__main__":
    app.run()