from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'friends are allowed to access private members'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [DataRequired()])
    email = StringField('What is your University of Toronto email?', validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        
        if old_name is None and old_email is None:
            session['name'] = ''
            session['email'] = ''

        if "@mail.utoronto.ca" not in form.email.data:
            flash("Not a valid email")
            session['name'] = old_name
            session['email'] = old_email
            return redirect(url_for('index'))

        if old_name is not None and old_name != form.name.data and "utoronto" in form.email.data:
            flash("Looks like you have changed your name!")

        session['name'] = form.name.data
        session['email'] = form.email.data
        form.name.data = ''
        form.email.data = ''

        return redirect(url_for('index'))
    return render_template('index.html', form = form, current_time = datetime.now(), name = session.get('name'), email = session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=True)