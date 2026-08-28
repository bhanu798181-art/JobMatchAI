from database import Base, engine
from external_jobs.models import ExternalJob


print("Creating external_jobs table...")

Base.metadata.create_all(
    bind=engine,
    tables=[
        ExternalJob.__table__
    ]
)

print("external_jobs table is ready.")