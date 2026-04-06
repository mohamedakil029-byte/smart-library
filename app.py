"""Main Application Entry Point"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import config
from database import init_db
from models import User
import os


def create_app(config_name: str = None) -> Flask:
    """
    Application factory function
    
    Args:
        config_name: Configuration environment (development, testing, production)
        
    Returns:
        Flask application instance
    """
    
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    cfg = config.get(config_name) or config['default']
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(cfg)
    
    # Initialize database
    engine, SessionLocal = init_db(app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Store session factory for later use
    app.SessionLocal = SessionLocal
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        db = SessionLocal()
        try:
            return db.query(User).get(int(user_id))
        finally:
            db.close()
    
    # Import and register API routes
    from api import register_api_routes
    register_api_routes(app, SessionLocal)
    
    # Web UI routes
    @app.route('/', methods=['GET'])
    @login_required
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            db = SessionLocal()
            try:
                user = db.query(User).filter_by(username=username).first()
                if user and user.check_password(password):
                    login_user(user)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('index'))
                else:
                    flash('Invalid username or password')
            finally:
                db.close()
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            
            db = SessionLocal()
            try:
                # Check if user already exists
                existing_user = db.query(User).filter(
                    (User.username == username) | (User.email == email)
                ).first()
                
                if existing_user:
                    flash('Username or email already exists')
                else:
                    user = User(
                        username=username,
                        email=email,
                        full_name=full_name
                    )
                    user.set_password(password)
                    db.add(user)
                    db.commit()
                    flash('Registration successful! Please log in.')
                    return redirect(url_for('login'))
            finally:
                db.close()
        
        return render_template('register.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'Smart Library Request Workflow'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
