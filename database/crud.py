from database.models import Base
from database.db_setup import engine

Base.metadata.create_all(engine)
print("database tables created")


from sqlalchemy.orm import sessionmaker  # type: ignore

Session = sessionmaker(bind=engine)
session = Session()
print("session ready")
