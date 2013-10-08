from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required

class LoginForm(Form):
    zip1 = TextField('zip1', validators = [Required()])
    zip2 = TextField('zip2', validators = [Required()])
    housing = SelectField('Rent or Buy?', choices = [('rent','Rent'),('buy','Buy')])
