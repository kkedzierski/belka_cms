from flask import redirect, render_template
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/sign_in')
def sign_in():
    return render_template("sign_in/sign_in.html")