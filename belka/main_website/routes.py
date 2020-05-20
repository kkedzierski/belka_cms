from flask import render_template, Blueprint


website = Blueprint('website', __name__)


@website.route('/index')
def index():
    return render_template('main_website/index.html', title="index")
