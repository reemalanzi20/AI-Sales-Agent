from app.database.database import Base, engine
from app.models.booking import Booking

Base.metadata.create_all(bind=engine)

print("Database created successfully!")