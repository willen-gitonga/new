from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required


class PitchForm(FlaskForm):
    # title = StringField('Comment title', validators=[Required()])
    content = TextAreaField('New Pitch')
    # comment = TextAreaField('New Pitch')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    title = StringField('Comment title', validators=[Required()])
    comment_content = TextAreaField('New Comment')
    submit = SubmitField('Submit')
