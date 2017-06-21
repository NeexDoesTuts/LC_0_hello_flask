# Hello Flask
These are notes created wile followng along LC101 Web Dev tutorial: Hello-Flask.

## Get virtual environment set-up

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

### Explanations

* `from flask import Flask`: this imports the `Flask` class from the `flask` module.
* `app = Flask(__name__)`: app will be the object created by the constructor `Flask`. `__name__` is a variable controlled by Python that tells code what module it's in.
* `app.config['DEBUG'] = True`: the `DEBUG` configuration setting for the Flask application will be enabled. This enables some behaviors that are helpful when developing Flask apps, such as displaying errors in the browser, and ensuring file changes are reloaded while the server is running (aka "host swapping")
* `@app.route("/")`: this is a decorator that creates a mapping between the path - in this case the root, or "/", and the function that we're about to define
* `def index():`: Ah, familiar ground! We define `index`, a function of zero variables
* `return "Hello World"`: Our function returns a string literal.
* `app.run()`: Pass control to the Flask object. The run function loops forever and never returns, so put it last. It carries out the responsibilities of a web server, listening for requests and sending responses over a network connection.

## Forms

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

### Forms in Flask

The `name` attribute of a form element determines the key that will be used to pass the parameter to the server in the HTTP request. Thus, if an element has `name='first_name'` then the string `'first_name'` must be used to access the value of the form element on the server.

```python
# add request object to imported elements
from flask import Flask, request
```

#### Accessing GET request parameters

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

#### Accessing POST request parameters

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

#### 405 - Method Not Allowed

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

#### Accessing form data

```python
@app.route("/form-inputs", methods=["POST"])
def print_form_values():
    response = ""
    for field in request.form.keys():
        response += "<b>{key}</b>: {value}<br>".format(key=field, value=request.form[field])
    return response
```

#### Data displayed:

> **user-name**: text-field
> **user-password**: password-field
> **user-email**: email@email.com
> **shopping-cart-id**: 0129384
> **cb1**: first-cb
> **cb2**: second-cb
> **coffee-size**: med
> **life-story**: Ketchup and Mustard were both picked
> **lc-hub**: mia

Alert! If cb1 had no value, it would only say: `cb1: on` and if it was not picked, it would not be there at all.

#### .format() method

##### Using indexed placeholders

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

##### Using named placeholders

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





#### Validation

#### Redirects

#### HTML escaping

```python
import cgi
cgi.escape(<variable_from_user_input>)
```


