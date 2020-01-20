# LTRCOL-2574 Sample Portal

The following contains a sample web portal with skeleton code that allows you to perform certain administrative and/or user functions on Cisco Unified Collaboration products.

## Steps to start

### Step 1

Make sure python3 is installed (```python --version```).  You may also install/use a virtual environment.  

### Step 2

Install all python requirements with:

```pip install -r requirements.txt```

### Step 3

Now you need to start the web service with ```python -m flask run``` in order to start the Flask development server. 

### Step 4

The web server is ready once these messages appear:

```
 * Serving Flask app "flaskr" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 255-014-512
 ```

### Step 5

In your browser, access the page using `http://localhost:5000`

## VS Code Setup ##

in your launch.json, to set breakpoints and debugs, you should have an entry such as:

```
        {
            "name": "Start LTRCOL-2574 Portal",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--host=0.0.0.0",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        },        
```
