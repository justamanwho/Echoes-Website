from database import SessionLocal
from models import User


db = SessionLocal()

existing = db.query(User).filter(User.api_key == "test").first()
if existing:
    print("User already exists.")
else:
    user = User(
        username="admin",
        email="admin@example.com",
        api_key="test",
        is_verified=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    print("User created.")
