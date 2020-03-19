from flask import render_template, flash, redirect, url_for, send_from_directory
from app import app, db
from app.forms import LoginForm, EditForm, RemoveForm #to login, to edit, to remove
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User, Post
from flask import request
from werkzeug.urls import url_parse
from flask import send_file

@app.route('/')
@app.route('/index')
def index():
	#posts = Post.query.order_by(Post.timestamp.desc()).paginate(1, 20, False).items
	page = request.args.get('page', 1, type=int)
	#Displays the posts in reverse chronological order
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	
	#Navigates to next and previous url if they exist
	if posts.has_next:
		next_url = url_for('index', page=posts.next_num)
	else:
		next_url = None
	if posts.has_prev:
		prev_url = url_for('index', page=posts.prev_num)
	else:
		prev_url = None
	return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		#stores the information submitted and then can display it as a message in the redirected page
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		next_page =  request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		login_user(user)
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	form = EditForm()
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		#p = Post(title = str(form.title), body = str(form.text), author = current_user)
		#textList = str(form.title).split('"')
		#postTitle = textList[-2] #string splitting gets the actual title of the post
		#bodyList = str(form.text).split('>')
		#bodyList2 = bodyList[1].split('<')
		#postBody = bodyList2[0] #string splitting gets the actual body of the post
		q = Post(title=str(form.title.data), body=str(form.text.data), author=current_user)
		db.session.add(q)
		db.session.commit()
		flash('Post created successfully. ID = ' + str(q.id))
		return redirect(url_for('index'))
	return render_template('edit.html', title='Add Post', form=form)

@app.route('/resume')
def resume():
	#return send_from_directory(directory='/app', filename='cv.pdf', mimetype='application.pdf')
	return render_template('resume.html', title='Contact')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
	form = RemoveForm()
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		try:
			p = Post.query.get(int(form.number.data))
			db.session.delete(p)
			db.session.commit()
			flash('Post ' + str(form.number.data) + ' removed successfully')
		except:
			flash('Post ' + str(form.number.data) + ' does not exist.')
		return redirect(url_for('index'))
	return render_template('remove.html', title='Remove', form=form)

@app.route('/tutoring')
def tutoring():
	return render_template('tutoring.html', title='Tutoring')

@app.route('/credits')
def credits():
	return render_template('credits.html', title='Credits')

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/return-file')
def return_file():
	#working code, but not now
	#try:
	#	return send_file('cv.pdf')
	#except Exception as e:
	#	return str(e)
	return render_template('about.html', title='About') #go back to About, for privacy
