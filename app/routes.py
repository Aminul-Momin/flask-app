from app import app, db, bcrypt
from flask import redirect, render_template, url_for, flash
#==============================================================================
from app.forms import RegisterForm, LoginForm, PostForm
from app.models import User, Post
#==============================================================================

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))

    if form.validate_on_submit():
        is_email_taken = User.query.filter_by(email=form.email.data).first()

        if is_email_taken:
            flash(f"Please choose different email. It's taken already !", 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    flash('You have been loged out', 'success')
    return redirect(url_for('home'))


@app.route('/post/new', methods=['GET','POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('create_post.html', form=form, Title='New Post', legend='New Post')