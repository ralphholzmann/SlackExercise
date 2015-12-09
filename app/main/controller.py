from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from flask import render_template, request, session, redirect, jsonify

from forms import WebPageForm

from . import main

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
    return render_template('index.html', form=form)

@main.route('/pagesummary', methods=['POST'])
def pagesummary():
    form = WebPageForm()
    response = {}
    if form.validate_on_submit():
        url = str(form.url_field.data)
        html_source, summary = _get_html_summary(url)
        response['source'] = html_source
        response['summary'] = summary
    return jsonify(**response)

@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
