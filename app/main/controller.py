from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from flask import render_template, request, session, redirect
from flask.ext.wtf import Form
from wtforms.validators import Required, url
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import URLField

from . import main

class WebPageForm(Form):
    url_field = URLField('URL', validators=[Required(), url()])
    fetch_field = SubmitField('Fetch')

def _get_html_summary(url):
    EMPTY = (None, None)
    if not url:
        return EMPTY
    r = requests.get(url)
    if not r or r.status_code != 200:
        return EMPTY
    parser = BeautifulSoup(r.text, 'html.parser')
    src = parser.prettify()
    tag_counts = defaultdict(int)
    for tag in parser.findAll():
        tag_counts[tag.name] += 1
    return src, tag_counts

@main.route('/', methods=['GET', 'POST'])
def index():
    form = WebPageForm()
    html_source = None
    summary = {}
    if form.validate_on_submit(): # Post request with valid form
        session['url'] = str(form.url_field.data)
        return redirect('/') # Avoid form resubmission
    url = session.get('url')
    if url:
        html_source, summary = _get_html_summary(url)
        session.pop('url')
    return render_template('index.html', form=form, source=html_source, summary=summary)

@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
