from sqlalchemy import create_engine

# Import models so that they get registered with Base.metadata
from models import Base, Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')

Base.metadata.create_all(engine)

print("✅ freebies.db created and tables initialized!")
