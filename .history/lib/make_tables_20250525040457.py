from models import Base
from sqlalchemy import create_engine

# Connect to the SQLite database
engine = create_engine('sqlite:///db/freebies.db')

# Create tables based on the models
Base.metadata.create_all(engine)

print("✅ Tables created successfully!")
