from flask import render_template,redirect,url_for,abort
from . import main
from ..models import Category,Comment,User,Pitch
# from ..models import get_category
from flask_login import login_required
from .forms import CommentForm
from .. import db
from .forms import PitchForm,CommentForm


@main.route('/')
def index():
    '''
    landing page
    '''
    title = 'Minute pitch'
    category = Category.get_category()
  
    return render_template('index.html', title = title,category=category)


@main.route("/pitches/<category>")
def categories(category):
    pitches = None
    if category == "all":
        pitches = Pitch.query.order_by(Pitch.time.desc())

    else:
        pitches = Pitch.query.filter_by(category = category).order_by(Pitch.time.desc()).all()


    return render_template("pitch.html",pitches = pitches)



@main.route('/pitch/<int:id>', methods =['GET','POST'])
@login_required
def one_pitch(id):

    pitches = Pitch.query.get(id)
    comments = Comment.get_comments(id)

    return render_template('one_pitch.html', pitches=pitches,comments=comments)




@main.route('/categories/pitch/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_pitch(id):


    form = PitchForm()
    category = Category.query.get(id)
    comment = Comment.get_comments(id)

    if form.validate_on_submit():
        content = form.content.data

        new_pitch = Pitch(content=content,category_id=category.id)
        new_pitch.save_pitches()
        return redirect(url_for('.categories', id = category.id))


    return render_template ('new_pitches.html',pitch_form=form)





@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


# comment section
@main.route('/categories/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):

    form = CommentForm()
    pitches = Pitch.query.get(id)
    # comment_content = []

    if form.validate_on_submit():
        title = form.title.data
        comment_content = form.comment_content.data

        new_comment = Comment(pitch_id=pitches.id,comment_content=comment_content)
        new_comment.save_comment()
        return redirect(url_for('.one_pitch',id=pitches.id))


    return render_template('new_comment.html',comment_form=form)
