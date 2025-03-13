from app import create_app
from app.services import facade
from werkzeug.security import generate_password_hash

def create_admin_user():
    """Create an admin user if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = facade.get_user_by_email('admin@example.com')
        if admin:
            print("Admin user already exists!")
            return
        
        # Admin user data
        admin_data = {
            'email': 'admin@example.com',
            'password': 'Admin123!',  # You should change this password
            'first_name': 'Admin',
            'last_name': 'User',
            'is_admin': True
        }
        
        try:
            admin = facade.create_user(admin_data)
            print(f"Admin user created successfully! ID: {admin.id}")
            print("Email: admin@example.com")
            print("Password: Admin123!")
        except Exception as e:
            print(f"Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin_user()
