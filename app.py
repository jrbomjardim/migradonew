from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://flashcards_user:flashcards_password@localhost/flashcards_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do email
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)
CORS(app)

# Modelos do banco de dados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    trial_start = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_end = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    flashcards = db.relationship('Flashcard', backref='author', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def is_trial_active(self):
        return datetime.utcnow() < self.trial_start + timedelta(hours=24)
    
    def is_subscription_active(self):
        return self.subscription_end and datetime.utcnow() < self.subscription_end

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    flashcards = db.relationship('Flashcard', backref='category', lazy=True)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    review_date = db.Column(db.DateTime)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas principais
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')     
        if User.query.filter_by(username=username).first():
            flash("Nome de usuário já existe.", "danger")
            return redirect(url_for("register"))
        
        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "danger")
            return redirect(url_for("register"))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash("Conta criada com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Verificar se o usuário tem acesso
    if not current_user.is_trial_active() and not current_user.is_subscription_active():
        return redirect(url_for('payment'))
    
    # Estatísticas do usuário
    total_cards = Flashcard.query.filter_by(user_id=current_user.id).count()
    cards_today = Flashcard.query.filter_by(user_id=current_user.id).filter(
        Flashcard.created_at >= datetime.utcnow().date()
    ).count()
    
    return render_template('dashboard.html', 
                         total_cards=total_cards, 
                         cards_today=cards_today)

@app.route('/payment')
@login_required
def payment():
    return render_template('payment.html')

@app.route('/flashcards')
@login_required
def flashcards():
    if not current_user.is_trial_active() and not current_user.is_subscription_active():
        return redirect(url_for('payment'))
    
    cards = Flashcard.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.all()
    return render_template('flashcards.html', cards=cards, categories=categories)

@app.route('/study')
@login_required
def study():
    if not current_user.is_trial_active() and not current_user.is_subscription_active():
        return redirect(url_for('payment'))
    
    categories = Category.query.all()
    return render_template('study.html', categories=categories)

@app.route('/community')
@login_required
def community():
    if not current_user.is_trial_active() and not current_user.is_subscription_active():
        return redirect(url_for('payment'))
    
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('community.html', posts=posts)

@app.route('/reports')
@login_required
def reports():
    if not current_user.is_trial_active() and not current_user.is_subscription_active():
        return redirect(url_for('payment'))
    
    return render_template('reports.html')

# API Routes
@app.route('/api/flashcards', methods=['GET', 'POST'])
@login_required
def api_flashcards():
    if request.method == 'POST':
        data = request.get_json()
        card = Flashcard(
            question=data['question'],
            answer=data['answer'],
            category_id=data['category_id'],
            user_id=current_user.id
        )
        db.session.add(card)
        db.session.commit()
        return jsonify({'message': 'Flashcard created successfully'}), 201
    
    cards = Flashcard.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': card.id,
        'question': card.question,
        'answer': card.answer,
        'category': card.category.name
    } for card in cards])

@app.route('/api/categories')
@login_required
def api_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name
    } for cat in categories])










if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Criar categorias padrão se não existirem
        if not Category.query.first():
            categories = [
                'Medicina Interna',
                'Cirurgia',
                'Pediatria',
                'Gineco e Obstetriz',
                'Perguntas do Grado'
            ]
            for cat_name in categories:
                category = Category(name=cat_name)
                db.session.add(category)
            db.session.commit()

