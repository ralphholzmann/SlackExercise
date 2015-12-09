from flask.ext.wtf import Form
from wtforms.validators import Required, url
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import URLField

class WebPageForm(Form):
    url_field = URLField('URL', validators=[Required(), url()])
    submit_field = SubmitField('Fetch')
