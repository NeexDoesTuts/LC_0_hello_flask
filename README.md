- [Get virtual environment set-up](#get-virtual-environment-set-up)
    - [Build main.py file](#build-main-py-file)
    - [Explanation to Hello-Flask code](#explanation-to-hello-flask-code)
- [Forms](#forms)
    - [Forms in Flask](#forms-in-flask)
        - [Accessing GET request parameters](#accessing-get-request-parameters)
        - [Accessing POST request parameters](#accessing-post-request-parameters)
        - [405 - Method Not Allowed](#405-method-not-allowed)
    - [Form inputs](#form-inputs)
        - [Accessing form data](#accessing-form-data)
        - [The .format() method](#the-format-method)
            - [Using indexed placeholders](#using-indexed-placeholders)
            - [Using named placeholders](#using-named-placeholders)
- [Validation](#validation)
    - [Server-side validation](#server-side-validation)
    - [Redirects](#redirects)
- [HTML escaping](#html-escaping)
- [Templates](#templates)
    - [Method with Jijna2 + specifying template directory](#method-with-jijna2-specifying-template-directory)
- [Jinja if/else + loop -> TODO app](#jinja-if-else-loop-todo-app)
# Get virtual environment set-up

```bash
conda create -n <env-name> 
source activate <env-name>
conda install flask
# optionally list packages to install right away
conda create -n <env-name> flask
```

Create or update (it will be overwritten) requirements file:

```bash
# activate environment:
source activate <env-name>
# export packages to a file:
# both conda and pip
conda env export > environment.yml

# recreate:
conda env create -f environment.yml
# It will use the other name, otherwise specify your own:
conda env create -f environment.yml -n new-name
```

## Build main.py file

```python
from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return "Hello World"

if __name__ == "__main__":
    app.run()
```

```bash
python main.py
```

## Explanation to Hello-Flask code

* `from flask import Flask`: this imports the `Flask` class from the `flask` module.
* `app = Flask(__name__)`: app will be the object created by the constructor `Flask`. `__name__` is a variable controlled by Python that tells code what module it's in.
* `app.config['DEBUG'] = True`: the `DEBUG` configuration setting for the Flask application will be enabled. This enables some behaviors that are helpful when developing Flask apps, such as displaying errors in the browser, and ensuring file changes are reloaded while the server is running (aka "host swapping")
* `@app.route("/")`: this is a decorator that creates a mapping between the path - in this case the root, or "/", and the function that we're about to define
* `def index():`: Ah, familiar ground! We define `index`, a function of zero variables
* `return "Hello World"`: Our function returns a string literal.
* `app.run()`: Pass control to the Flask object. The run function loops forever and never returns, so put it last. It carries out the responsibilities of a web server, listening for requests and sending responses over a network connection.

# Forms

```html
<form action="http://duckduckgo.com" method="GET"> 
  <input type="text" name="query">
  <input type="submit">
</form>
```

* **By default**, the `action` of a form is the same URL that the form is displayed at. Otherwise it specifies where to submit it.
* **By default**, the `method` of a form is `GET`.
* The `name` attribute of a form element determines the **key** that will be used to pass the parameter to the server in the HTTP request. Thus, if an element has `name='query'` then the string `'query'` must be used to access the value of the form element on the server.
* Accessing both `GET` and `POST` parameters within Flask requires the `request` object. **The request object** is provided by Flask, but it must be imported.

```html
<label for="query">Search something:</label>
<input type="text" name="q" id="query">
```

* The label uses `for=""` to link to a specific input. The input must have `id=""` equal to the same value as the label. It is usual the same as name, but technically, it does not have to be. 

## Forms in Flask

The `name` attribute of a form element determines the key that will be used to pass the parameter to the server in the HTTP request. Thus, if an element has `name='first_name'` then the string `'first_name'` must be used to access the value of the form element on the server.

```python
# add request object to imported elements
from flask import Flask, request
```

### Accessing GET request parameters

A query (or `GET` request) parameter can be accessed via `request.args`:

```python
form_value = request.args.get('param_name')
```

`GET` parameters are passed in the HTTP request as part of the URL. More specifically, they make up the query string--the portion after `?`--which looked like this in the lesson:

```python
http://localhost:5000/hello?first_name=Chris
```

Here, the query string is `?first_name=Chris`. If there were multiple query parameters, they would be separated by the `&` (ampersand) character.

```python
http://localhost:5000/hello?first_name=Chris&last_name=Bay
```

### Accessing POST request parameters

To enable a handler function to receive `POST` requests, we must add a `methods` parameter to the `@app.route` decorator:

```python
@app.route('/path', methods=['POST'])
def my_handler():
    # request handling code
```

A `POST` parameter can be accessed via `request.form`:

```python
# request.form is a dictionary-like object
form_value = request.form['param_name']
```

### 405 - Method Not Allowed

An HTTP status of 405 - Method Not Allowed will be received if a resource/path is requested that doesn't accept requests using the given method (usually, `GET` or `POST`). This can be a common mistake when setting up a form to `POST` to a given path, but failing to configure the handler function to accept `POST` requests.

## Form inputs

Notice especially the hidden input.

```html
<form method='POST'>
    <label>type=text
        <input name="user-name" type="text" />
    </label>
    <label>type=password
        <input name="user-password" type="password" />
    </label>
    <label>type=email
        <input name="user-email" type="email" />
    </label>
    <!-- hidden input -->
  	<input name="shopping-cart-id" value="0129384" type="hidden" />
  
    <label>Ketchup
    	<input type="checkbox" name="cb1" value="first-cb" />
    </label>
    <label>Mustard
        <input type="checkbox" name="cb2" value="second-cb" />
    </label>
    <label>Small
        <input type="radio" name="coffee-size" value="sm" />
    </label>
    <label>Medium
        <input type="radio" name="coffee-size" value="med" />
    </label>
    <label>Large
         <input type="radio" name="coffee-sizes" value="lg" />
    </label>
    <label>Your life story
        <textarea name="life-story"></textarea>
    </label>
    <label>LaunchCode Hub
            <select name="lc-hub">
                <option value="kc">Kansas City</option>
                <option value="mia">Miami</option>
                <option value="ri">Providence</option>
                <option value="sea">Seattle</option>
                <option value="pdx">Portland</option>
            </select>
        </label>
    <input type="submit" />
</form>
```

### Accessing form data

```python
@app.route("/form-inputs", methods=["POST"])
def print_form_values():
    response = ""
    for field in request.form.keys():
        response += "<b>{key}</b>: {value}<br>".format(key=field, value=request.form[field])
    return response
```

Example data from the form is displayed as:

**user-password**: password-field
**user-email**: email@email.com
**shopping-cart-id**: 0129384
**cb1**: first-cb
**cb2**: second-cb
**coffee-size**: med
**life-story**: Ketchup and Mustard were both picked
**lc-hub**: mia

Alert! If `cb1` had no value, it would only say: `cb1: on` and if it was not picked, it would not be there at all.

### The .format() method

#### Using indexed placeholders

The index can be reused.

```python
markup = """
<!doctype html>
<html>
    <head>
        <title>{0}</title>
    </head>
    <body>
        <h1>{0}-{1}</h1>
    </body>
</html>
"""

markup = markup.format('My Page Title', 'My Page Heading')
print(markup)
```

#### Using named placeholders

Order does not matter but the variable must be given.

```python
markup = """
<!doctype html>
<html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h1>{heading}</h1>
    </body>
</html>
"""

markup = markup.format(title='My Page Title', heading='My Page Heading')
print(markup)
```

# Validation

Validation is the process of checking data against requirements. The requirements might be chosen by the developer e.g.: max length for a username or a tweet. But also logical validity like range for dates, time, temperature, weight, age, addresses, phone numbers, credit card numbers, etc. 

Validation can happen both at the client side and server side. 

A lot of client side is embedded into HTML5, but can be extended to JavaScript, which lets users correct errors without making a server request.

Client side validation can be bypassed super easily, thus server side is a must.

## Server-side validation

The server-side validation is just a normal Python code checking data against desired requirements. Example of simple 24-hour clock validation:

```html
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
```

```python
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
        return "Success"
    else:
        return time_form.format(hours=hours,
                        hours_error=hours_error,
                        minutes=minutes,
                        minutes_error=minutes_error)
```

## Redirects

Using previous example, redirecting user when valid time is submitted:

```python
# must add:
from flask import redirect

(...)
if not minutes_error and not hours_error:
    return redirect("valid-time")
(...)

@app.route("/valid-time")
def valid_time():
    return "<h1>Thanks for submitting a valid time!</h1>"
```

The HTTP requests for redirect:

```bash
127.0.0.1 - - [22/Jun/2017 14:41:03] "POST /validate-time HTTP/1.1" 200 -
127.0.0.1 - - [22/Jun/2017 14:41:07] "POST /validate-time HTTP/1.1" 302 -
127.0.0.1 - - [22/Jun/2017 14:41:08] "GET /valid-time HTTP/1.1" 200 -
```

More advanced version with passing arguments:

```python
if not minutes_error and not hours_error:
    time = str(hours) + ":" + str(minutes)
    return redirect("valid-time?time={0}".format(time))
```

(...)

```python
@app.route("/valid-time")
def valid_time():
    time = request.args.get("time")
    return "<h1>You submitted {0}. Thanks for submitting a valid time!</h1>".format(time)
```

# HTML escaping

Any time user inputs data, one must assume the user wants to break our stuff with malicious, bad, terrible, argh stuff! 

Either by breaking HTML and adding tags, or inserting JavaScript, which can do real harm. Or worst trying to [drop database](https://xkcd.com/327/).

HTML escaping in Flask:

```python
# in imports, from Python standard library, not Flask:
import cgi

# for everything user inputs:
cgi.escape(variable_from_user_input)
```

`cgi` translates code into entities which browsers can display as text. For example:

```javascrit
<script>bad javascript stuff</script>
```

will be displayed as text:  &lt;script&gt;bad javascript stuff&lt;/script&gt;

# Templates

Flask uses Jinja2 templating language.

## Method with Jijna2 + specifying template directory

1. Adding Jinja to Flask
  ```python
  # add to imports
  import os
  import jinja2
  ```

2. Create `templates` folder in main app folder:
  ```
  *
  +-- templates
  +-- app.py
  ```

3. In app.py:
  ```python
  # create template directory
  # grab the location of the folder for the current file, and append "templates" 
  # as folder name 
  template_dir = os.path.join(os.path.dirname(__name__), "templates")
  # initialize jinja2 engine
  jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
  ```

4. Create template:
  ```
  *
  +-- templates
  	+-- hello_form.html
  +-- app.py
  ```

5. Use template:
  ```python
  @app.route("/")
  def index():
      # grab template relative to templates folder
      template = jinja_env.get_template("hello_form.html")
      return template.render()
  ```

6. Pass data to template from app.py:
  ```python
  @app.route("/hello")
  def hello():
      name = request.args.get('name')
      template = jinja_env.get_template("hello_greetings.html")
      return template.render(name=name) 
  	# first name is the one in template, second is the variable in app.py
  ```

  template:

  ```html
  <!doctype html>
  <html>
      <head>
          <title>Hello {{name}}</title>
      </head>
      <body>
          <h1>Hello, {{name}}!</h1>
      </body>
  </html>
  ```

  located in:

  ```
  *
  +-- templates
  	+-- hello_form.html
  	+-- hello_greetings.html
  +-- app.py
  ```
7. No need to pass values for empty strings unlike .format() before:
  ```python
  @app.route("/validate-time")
  def display_time_form():
      template = jinja_env.get_template("time_form.html")
      return template.render()
  ```

# Jinja if/else + loop -> TODO app

A simple TODO app shows the looping logic in Jinja in an easy to understand way:

```python
@app.route("/todos", methods=["POST", "GET"])
def todos():
    # check if you are here via POST, and add task:
    if request.method == "POST":
        task = request.form['task']
        tasks.append(task)

    template = jinja_env.get_template("todos.html")
    return template.render(tasks=tasks) # pass the list to template
```

The rout will check if it is a POST or GET (case sensitive) request, and if POST, add task to list of tasks. The task is passed to template:

```jinja2
<!doctype html>
<html>
    <head>
        <title>TODOs</title>
    </head>
    <body>
        <h1>TODOs</h1>
        <form action="" method="POST">
            <label for="task">
                New Task:
                <input type="text" name="task" id="task" />
            </label>
            <input type="submit" value="Add todo">
        </form>

        <hr />

        {% if tasks|length == 0 %}
        <p>No tasks yet</p>
        {% else %}

            <ul>
                {% for task in tasks %}
                <li>{{task}}</li>
                {% endfor %}
            </ul>

        {% endif %}

    </body>
</html>
```

In the template Jinja checks for task length (line 18) and displays `No tasks yet` when empty, or renders a list of tasks, if not empty.

The Jinja loop and if/else syntax requires `{% %}` and closing tags:

```jinja2
{% if tasks|length == 0 %}
<p>No tasks yet</p>
{% else %}
    <ul>
        {% for task in tasks %}
        <li>{{task}}</li>
        {% endfor %}
    </ul>
{% endif %}
```

