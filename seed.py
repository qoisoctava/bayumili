from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app("development")


def seed_admin():
    with app.app_context():
        # Check if admin already exists
        existing = User.query.filter_by(username="admin").first()
        if existing:
            print("⚠️  Admin user already exists, skipping...")
            return

        # Create admin user
        admin = User(
            username="admin",
            email="admin@bayumili.local",
        )
        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully!")
        print("   Username : admin")
        print("   Password : admin123")
        print("   ⚠️  Please change the password after first login!")


if __name__ == "__main__":
    seed_admin()
