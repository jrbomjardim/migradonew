#!/usr/bin/env python3
"""
WSGI config for flashcards project.
"""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app import app as application

# Initialize database tables on startup
with application.app_context():
    from app import db, Category
    try:
        db.create_all()
        
        # Create default categories if they don't exist
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
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == "__main__":
    application.run()

