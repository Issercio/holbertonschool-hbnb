from app import create_app, db
from app.models import User

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@hbnb.io').first():
            try:
                admin = User.create_user({
                    'email': 'admin@hbnb.io',
                    'password': 'admin_password',
                    'is_admin': True,
                    'first_name': 'Admin',
                    'last_name': 'User'
                })
                print("Admin user created successfully.")
            except ValueError as e:
                print(f"Error creating admin user: {str(e)}")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
