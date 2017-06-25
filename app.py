from flask import Flask, request, redirect
import os
import jinja2

# create template directory
# grab the location of the folder for the current file, and append "templates" 
# as folder name 
template_dir = os.path.join(os.path.dirname(__name__), "templates")
# initialize jinja2 engine
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config["DEBUG"] = True

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

@app.route("/")
def index():
    # grab template relative to templates folder
    template = jinja_env.get_template("hello_form.html")
    return template.render()

@app.route("/hello")
def hello():
    name = request.args.get('name')
    template = jinja_env.get_template("hello_greetings.html")
    return template.render(name=name)

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
    template = jinja_env.get_template("time_form.html")
    return template.render() # does not need empty values, like .format() does

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
        template = jinja_env.get_template("time_form.html")
        return template.render(hours=hours,
                                hours_error=hours_error,
                                minutes=minutes,
                                minutes_error=minutes_error)

@app.route("/valid-time")
def valid_time():
    time = request.args.get("time")
    return "<h1>You submitted {0}. Thanks for submitting a valid time!</h1>".format(time)


tasks = [] # keep tasks here for now

@app.route("/todos", methods=["POST", "GET"])
def todos():
    # check if you are here via POST, and add task:
    if request.method == "POST":
        task = request.form['task']
        tasks.append(task)

    template = jinja_env.get_template("todos.html")
    return template.render(title="TODOs", tasks=tasks) # pass the list to template

if __name__ == "__main__":
    app.run()