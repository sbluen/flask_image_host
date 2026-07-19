import posixpath
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import file
from flask_wtf import file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Image
from app.forms import LoginForm, RegisterForm, UploadForm
from datetime import datetime

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    images = Image.query.all()
    return render_template('index.html', images=images)

@main_bp.route('/gallery')
def gallery():
    if current_user.is_authenticated:
        images = current_user.images
    else:
        images = []
    return render_template('gallery.html', images=images)

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.file.data:
            file = form.file.data

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = posixpath.join(UPLOAD_FOLDER, filename)

                absolute_upload_dir = os.path.abspath(os.path.join(current_app.root_path, UPLOAD_FOLDER))
                native_file_path = os.path.join(absolute_upload_dir, filename)
                file.save(native_file_path)
                
                image = Image(
                    filename=file.filename,
                    file_path=file_path,
                    user_id=current_user.id,
                    title=form.title.data,
                    description=form.description.data
                )
                db.session.add(image)
                db.session.commit()
                flash('Image uploaded successfully!', 'success')
                return redirect(url_for('main.gallery'))
            else:
                flash('File type not allowed. Allowed types: png, jpg, jpeg, gif, webp', 'error')
    return render_template('upload.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('main.gallery'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@auth_bp.route('/' + UPLOAD_FOLDER + '/<path:filename>')
def get_image(filename):
    try:
        print(filename)
        # Securely fetch and return the file from the designated directory
        absolute_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
        return send_from_directory(absolute_path, filename)
    except FileNotFoundError:
        # Return a 404 error if the image file doesn't exist
        abort(404)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
