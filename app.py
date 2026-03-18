from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
import os
from flask_mail import Mail, Message

from models import db, User, Car, Image
from translations import TRANSLATIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'arifoglu-super-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail Configuration (Example using Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with yours
app.config['MAIL_PASSWORD'] = 'your-app-password'     # Replace with your app password
app.config['MAIL_DEFAULT_SENDER'] = 'info@arifoglu.car'

mail = Mail(app)

# Google OAuth Config
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', 'placeholder-id')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', 'placeholder-secret')

db.init_app(app)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # Note: API base URL is used for some providers
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize Database
with app.app_context():
    db.create_all()

# --- Language Support ---
@app.context_processor
def inject_translations():
    lang = session.get('lang', 'ENG')
    if lang not in TRANSLATIONS:
        lang = 'ENG'
    
    def translate(key):
        return TRANSLATIONS[lang].get(key, key)
        
    return dict(t=translate, current_lang=lang)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in TRANSLATIONS:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form.get('form_type') == 'contact':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Send Real Email
        mail_sent = False
        mail_error = None
        try:
            msg = Message(
                subject=f"Arifoglu: New message from {name}",
                recipients=['your-email@gmail.com'], # Replace with your destination
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            mail_sent = True
            print(f"DEBUG: Email sent successfully for {name}")
        except Exception as e:
            mail_error = str(e)
            print(f"DEBUG: Mail error: {mail_error}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if mail_sent:
                return {'status': 'success', 'message': TRANSLATIONS.get(session.get('lang', 'ENG'), {}).get('contact_success', 'Message sent successfully!')}
            else:
                return {'status': 'error', 'message': f'SMTP Error: {mail_error}. Make sure to set your real email and App Password in app.py.'}
            
        if mail_sent:
            flash('Message sent successfully!', 'success')
        else:
            flash(f'Error sending email: {mail_error}. Check your SMTP settings.', 'danger')
        return redirect(url_for('index') + '#contact')
    
    # Simple car search logic
    search_query = request.args.get('search', '').lower()
    brand = request.args.get('brand', '')
    model = request.args.get('model', '')
    max_price = request.args.get('max_price', type=int)
    
    query = Car.query
    
    if search_query:
        query = query.filter(Car.title.ilike(f'%{search_query}%'))
    if brand:
        query = query.filter(Car.brand.ilike(f'%{brand}%'))
    if model:
        query = query.filter(Car.model.ilike(f'%{model}%'))
    if max_price:
        query = query.filter(Car.price <= max_price)
        
    cars = query.order_by(Car.id.desc()).all()
    
    return render_template('index.html', cars=cars)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    if current_user.role != 'seller':
        flash('Only sellers can add car listings.', 'danger')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price', type=int)
        year = request.form.get('year', type=int)
        brand = request.form.get('brand')
        model = request.form.get('model')
        mileage = request.form.get('mileage', type=int)
        fuel_type = request.form.get('fuel_type')
        transmission = request.form.get('transmission')
        location = request.form.get('location')
        description = request.form.get('description')
        images = request.form.get('images', '') # comma separated URLs
        
        new_car = Car(
            title=title, price=price, year=year, brand=brand, model=model,
            mileage=mileage, fuel_type=fuel_type, transmission=transmission,
            location=location, description=description, seller_id=current_user.id
        )
        db.session.add(new_car)
        db.session.commit()
        
        # Add Images
        if images:
            image_urls = [url.strip() for url in images.split(',') if url.strip()]
            for url in image_urls:
                new_img = Image(car_id=new_car.id, image_url=url)
                db.session.add(new_img)
            db.session.commit()
            
        flash('Car listing added successfully!', 'success')
        return redirect(url_for('car_detail', car_id=new_car.id))
        
    return render_template('add_car.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'login':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Welcome back!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid email or password.', 'danger')
                
        elif action == 'register':
            name = request.form.get('name')
            surname = request.form.get('surname')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role', 'buyer')
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already registered.', 'danger')
            else:
                hashed_pw = generate_password_hash(password, method='scrypt')
                new_user = User(name=name, surname=surname, email=email, password_hash=hashed_pw, role=role)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                flash('Registration successful!', 'success')
                return redirect(url_for('index'))
                
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/google-login')
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/google-callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    if not user_info:
        # Fallback for some providers if userinfo is not in token
        user_info = google.get('userinfo').json()
    
    email = user_info.get('email')
    google_id = user_info.get('sub')
    name = user_info.get('given_name')
    surname = user_info.get('family_name')
    picture = user_info.get('picture')

    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        # Check if user exists with same email but no google_id
        user = User.query.filter_by(email=email).first()
        if user:
            user.google_id = google_id
            if picture and not user.profile_photo:
                user.profile_photo = picture
        else:
            # Create new user
            user = User(
                email=email,
                google_id=google_id,
                name=name,
                surname=surname,
                profile_photo=picture,
                role='buyer' # Default role
            )
            db.session.add(user)
    
    db.session.commit()
    login_user(user)
    flash(f'Welcome back, {user.name}!', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    user_listings = Car.query.filter_by(seller_id=current_user.id).order_by(Car.id.desc()).all()
    favorite_cars = current_user.favorite_cars
    return render_template('profile.html', user_listings=user_listings, favorite_cars=favorite_cars)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            current_user.name = request.form.get('name')
            current_user.surname = request.form.get('surname')
            current_user.email = request.form.get('email')
            current_user.profile_photo = request.form.get('profile_photo')
            
            # Persistent language preference logic
            lang = request.form.get('lang')
            if lang in TRANSLATIONS:
                session['lang'] = lang
                
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            
        elif action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not check_password_hash(current_user.password_hash, current_password):
                flash('Incorrect current password.', 'danger')
            elif new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
            else:
                current_user.password_hash = generate_password_hash(new_password, method='scrypt')
                db.session.commit()
                flash('Password updated successfully!', 'success')
                
        return redirect(url_for('settings'))
    return render_template('settings.html')

@app.route('/toggle_favorite/<int:car_id>', methods=['POST'])
@login_required
def toggle_favorite(car_id):
    car = Car.query.get_or_404(car_id)
    if car in current_user.favorite_cars:
        current_user.favorite_cars.remove(car)
        status = 'removed'
    else:
        current_user.favorite_cars.append(car)
        status = 'added'
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return {'status': status}
    
    return redirect(request.referrer or url_for('index'))

@app.route('/calculator')
def calculator():
    return render_template('calculator.html', **inject_translations())

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Redirect to home page's contact section for unified MVP experience
    return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
