import os
import sys
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.Core.Database.ApplicationDatabaseContext import ApplicationDatabaseContext
from app.Core.Config.settings import settings
from app.Core.Security.PasswordManager import PasswordManager
from app.Entities.Base.User import User
from app.Repositories.User.UserRepository import UserRepository


def seed_admin_user():
    print("--- Running Admin User Seeder ---")
    db_context = ApplicationDatabaseContext(settings.database_url)
    db: Session = next(db_context.get_db())
    
    try:
        user_repository = UserRepository(db)
        
        admin_username = settings.ADMIN_USERNAME
        admin_password = settings.ADMIN_PASSWORD
        
        existing_admin = user_repository.get_by_username(admin_username)
        
        if existing_admin:
            print(f"Admin user '{admin_username}' already exists. Skipping.")
            return

        print(f"Admin user '{admin_username}' not found. Creating...")
        
        hashed_password = PasswordManager.get_password_hash(admin_password)
        
        new_admin = User(
            user_name=admin_username,
            hashed_password=hashed_password,
            is_admin=True
        )
        
        db.add(new_admin)
        db.commit()
        
        print("Admin user created successfully.")
        
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        print("--- Seeder Finished ---")
        db.close()

if __name__ == "__main__":
    seed_admin_user()