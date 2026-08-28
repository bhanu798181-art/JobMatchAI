import os
import sys
from datetime import date, timedelta


# --------------------------------------------------
# Make backend imports work
# --------------------------------------------------

BACKEND_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


# --------------------------------------------------
# Database imports
# --------------------------------------------------

from database import SessionLocal
from external_jobs.models import ExternalJob


# --------------------------------------------------
# Expiry configuration
# --------------------------------------------------

JOB_EXPIRY_DAYS = 30


# --------------------------------------------------
# Expire old jobs
# --------------------------------------------------

def expire_old_jobs():

    db = SessionLocal()

    try:

        expiry_date = (
            date.today()
            - timedelta(
                days=JOB_EXPIRY_DAYS
            )
        )

        old_jobs = (
            db.query(ExternalJob)
            .filter(
                ExternalJob.status == "active",
                ExternalJob.posted_date.isnot(None),
                ExternalJob.posted_date < expiry_date
            )
            .all()
        )

        expired_count = 0

        for job in old_jobs:

            job.status = "expired"

            expired_count += 1

        db.commit()

        print(
            f"Expired jobs: {expired_count}"
        )

        return expired_count

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("JOBMATCH AI - JOB EXPIRY CLEANUP")
    print("=" * 60)

    expire_old_jobs()

    print("=" * 60)
    print("CLEANUP COMPLETED")
    print("=" * 60)