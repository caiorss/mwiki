"""Login module - contains decoreators for login."""

import flask
from flask import Flask, session, request
from . import utils
from . models import User, Settings
from . constants import USER_ADMIN, USER_ADMIN, USER_ANONYMOUS, USER_EDITOR, USER_GUEST
from . constants import M_GET, M_POST, M_DELETE

def check_login_db(username: str, password: str) -> bool:
    ### print(" [TRACE] Enter check_login_db")
    res = User.get_user_by_username(username) 
    if res is None: 
        ##print(" [TRACE] Exit(1) check_login_db() ")
        ## breakpoint()
        return False
    ## breakpoint()
    if username == "admin" and res.password is None:
        dpassword = Settings.get_instance().default_password
        out = password == dpassword
    else:
        check = res.check_password(password) 
        out = res.active and check
    return out 


def add_login(app: Flask, do_login: bool, username: str, password: str):
    """Create login form routes for a single user account

    :param do_login: Flag - if set to true, login form is enabled, otherwise login form is disabled.
    :param username: Username required for authentication
    :param password: Corresponding password required for user authentication.
    :returns:        Function decorator for enforcing user authentication.

    Required Python Pakages: flask_session 
    
    This function creates a login form for a single user account by defining 
    the following http routes 

    /login  => Login form, where the user is redirect to in views/routes 
               that requeries authentication if the user is not logged in.

    /loggof => Logs off user and redirects to '/' root page of the site.

    This function returns a decorator function check_login, that can 
    be added to routes/views for requiring authentication. 

    Usage example:
     
    ```python

       app = Flask(__name__)

       LOGIN_ENABLED = True 

       # Creates login form for single user account 
       # requiring "dummy" as username and "pass" as password
       # for authentication.
       check_login = add_login(app, LOGIN_ENABLED, "dummy", "pass")
       
       # Require login for accessing http://<site-url>/check
       @app.route("/check")
       @check_login 
       def hello():
           return "The server is up and running. OK."
    ```

    """
    def is_loggedin():
        return session.get("loggedin") or False

    def do_login():
        session["loggedin"] = True

    def do_logoff():
        session["loggedin"] = False

    @app.route("/api/logged", methods = (M_GET, ))
    def api_is_logged_in():
        res =  session.get("loggedin") or False
        output = flask.jsonify({ "logged": res})
        return output

    @app.route("/login", methods = (M_GET, M_POST))
    def login():
        ## if not do_login:
        ##     return flask.redirect("/")
        ### breakpoint()
        path = utils.escape_url(request.args.get("path", "/"))
        if request.method == M_GET:
            if is_loggedin(): 
                ## breakpoint()
                return flask.redirect(path)
            else:
                return flask.render_template('login.html', path = path)
        assert request.method == M_POST
        _username = flask.request.form.get("username") or ""
        _password = flask.request.form.get("password") or ""
        print(f" [TRACE] _username = {_username} ; _password = {_password}")
        ##if _username == username and _password == password:
        ## breakpoint()
        if check_login_db(_username, _password): 
            do_login() 
            user = User.get_user_by_username(_username)
            session["user"] = user.to_Dict()
            return flask.redirect(path) 
        else:
            return flask.redirect(f"/login?path={path}")

    @app.route("/logoff")
    def loggof():
        do_logoff()
        session.clear()
        is_public = Settings.get_instance().public
        ## breakpoint()
        if is_public:
            path = request.args.get("path", "/")
            return flask.redirect(path)
        return flask.redirect("/login")

    def check_login(required = False):
        """Decorator that redirects to /login page if the user is not loggged in.
        The user is not asked to log in if the Wiki if the user is already authenticated
        or the wiki public. If the flag required is set to true, the user is asked to 
        log in regardless if the Wiki is public. Setting the flag required to true 
        is useful in pages where the user may modify data.
        """
        def login_checker(http_handler):
            def wrapper(*args, **kwargs):
                pass
                response = None
                is_public = Settings.get_instance().public
                ## breakpoint()
                loggedin = is_loggedin()
                if (is_public or loggedin) and (loggedin or not required):
                    response = http_handler(*args, **kwargs)
                else:
                    # Failed authentication / log in 
                    path = utils.escape_url(request.path)
                    response = flask.redirect(f"/login?path={path}") 
                    ## breakpoint()
                return response 
            wrapper.__name__ = http_handler.__name__
            return wrapper
        return login_checker
    return check_login

