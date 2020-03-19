from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class EditForm(FlaskForm):
	#title = TextField(u'Title', validators=[DataRequired()]) #Between 1 and 150 characters
	#text = TextAreaField(u'Text', validators=[DataRequired(), Length()]) #Between 1 and 5300 characters
	post = SubmitField('Post')
	title = TextField(u'Title', validators=[DataRequired(), Length(1, 150)]) #Between 1 and 150 characters
	text = TextAreaField(u'Text', validators=[DataRequired(), Length(1, 5300)]) #Between 1 and 5300 characters
class RemoveForm(FlaskForm):
	number = IntegerField(u'Post ID', validators=[DataRequired()]) #specifies the ID number of the post to be removed
	submit = SubmitField('Click to Remove')
