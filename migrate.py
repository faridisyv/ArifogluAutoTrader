from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text('ALTER TABLE user ADD COLUMN surname VARCHAR(50)'))
        print("Added surname column.")
    except Exception as e:
        print("Error adding surname:", e)
        
    try:
        db.session.execute(text('ALTER TABLE user ADD COLUMN profile_photo VARCHAR(255)'))
        print("Added profile_photo column.")
    except Exception as e:
        print("Error adding profile_photo:", e)

    try:
        db.session.execute(text('ALTER TABLE user ADD COLUMN google_id VARCHAR(100)'))
        print("Added google_id column.")
    except Exception as e:
        print("Error adding google_id:", e)
        
    db.session.commit()
    db.create_all()
    print("Re-ran create_all to ensure favorites table exists.")
