import os
import sys
from datetime import datetime


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
# Import Jooble collector
# --------------------------------------------------

from external_jobs.jooble import (
    fetch_jooble_jobs,
    save_jooble_jobs
)


# --------------------------------------------------
# Import Adzuna collector
# --------------------------------------------------

from external_jobs.adzuna import (
    fetch_adzuna_jobs,
    save_adzuna_jobs
)


# --------------------------------------------------
# Collection configuration
# --------------------------------------------------

SEARCHES = [
    {
        "keyword": "python developer",
        "location": "Hyderabad"
    },
    {
        "keyword": "java developer",
        "location": "Hyderabad"
    },
    {
        "keyword": "software developer",
        "location": "Hyderabad"
    },
    {
        "keyword": "web developer",
        "location": "Hyderabad"
    },
    {
        "keyword": "data analyst",
        "location": "Hyderabad"
    }
]


RESULTS_PER_PAGE = 10


# --------------------------------------------------
# Run collection
# --------------------------------------------------

def run_job_collection():

    start_time = datetime.now()

    total_received = 0
    total_saved = 0
    total_duplicates = 0
    successful_searches = 0
    failed_searches = 0

    print("=" * 60)
    print("JOBMATCH AI - JOB COLLECTION")
    print("=" * 60)

    print(
        "Started:",
        start_time.strftime("%Y-%m-%d %H:%M:%S")
    )

    print(
        f"Searches configured: {len(SEARCHES)}"
    )

    print(
        f"Results per search: {RESULTS_PER_PAGE}"
    )


    # ==================================================
    # JOOBLE COLLECTION
    # ==================================================

    print()
    print("=" * 60)
    print("JOOBLE COLLECTION")
    print("=" * 60)


    for index, search in enumerate(
        SEARCHES,
        start=1
    ):

        keyword = search["keyword"]
        location = search["location"]

        print()
        print("-" * 60)

        print(
            f"Jooble Search {index}/{len(SEARCHES)}"
        )

        print(
            f"Keyword : {keyword}"
        )

        print(
            f"Location: {location}"
        )

        print("-" * 60)


        try:

            # --------------------------------------------------
            # Fetch Jooble jobs
            # --------------------------------------------------

            jobs = fetch_jooble_jobs(
                keyword=keyword,
                location=location,
                results_per_page=RESULTS_PER_PAGE
            )

            received = len(jobs)

            print(
                f"Jobs received: {received}"
            )

            total_received += received


            # --------------------------------------------------
            # Save Jooble jobs
            # --------------------------------------------------

            saved, duplicates = (
                save_jooble_jobs(jobs)
            )

            print(
                f"New jobs saved: {saved}"
            )

            print(
                f"Duplicates found: {duplicates}"
            )

            total_saved += saved
            total_duplicates += duplicates

            successful_searches += 1

            print(
                "Jooble status: SUCCESS"
            )


        except Exception as error:

            failed_searches += 1

            print(
                "Jooble status: FAILED"
            )

            print(
                f"Jooble error: {error}"
            )

            # Continue with the next search
            continue


    # ==================================================
    # ADZUNA COLLECTION
    # ==================================================

    print()
    print("=" * 60)
    print("ADZUNA COLLECTION")
    print("=" * 60)


    for index, search in enumerate(
        SEARCHES,
        start=1
    ):

        keyword = search["keyword"]
        location = search["location"]

        print()
        print("-" * 60)

        print(
            f"Adzuna Search {index}/{len(SEARCHES)}"
        )

        print(
            f"Keyword : {keyword}"
        )

        print(
            f"Location: {location}"
        )

        print("-" * 60)


        try:

            # --------------------------------------------------
            # Fetch Adzuna jobs
            # --------------------------------------------------

            adzuna_jobs = fetch_adzuna_jobs(
                keyword=keyword,
                location=location,
                results_per_page=RESULTS_PER_PAGE
            )

            adzuna_received = len(
                adzuna_jobs
            )

            print(
                f"Adzuna jobs received: {adzuna_received}"
            )

            total_received += adzuna_received


            # --------------------------------------------------
            # Save Adzuna jobs
            # --------------------------------------------------

            adzuna_saved, adzuna_duplicates = (
                save_adzuna_jobs(
                    adzuna_jobs
                )
            )

            print(
                f"Adzuna new jobs saved: {adzuna_saved}"
            )

            print(
                f"Adzuna duplicates found: "
                f"{adzuna_duplicates}"
            )

            total_saved += adzuna_saved
            total_duplicates += adzuna_duplicates

            successful_searches += 1

            print(
                "Adzuna status: SUCCESS"
            )


        except Exception as error:

            failed_searches += 1

            print(
                "Adzuna status: FAILED"
            )

            print(
                f"Adzuna error: {error}"
            )

            # Continue with the next search
            continue


    # ==================================================
    # FINAL SUMMARY
    # ==================================================

    end_time = datetime.now()

    duration = (
        end_time - start_time
    ).total_seconds()


    print()
    print("=" * 60)
    print("COLLECTION COMPLETED")
    print("=" * 60)

    print(
        "Started:",
        start_time.strftime("%Y-%m-%d %H:%M:%S")
    )

    print(
        "Finished:",
        end_time.strftime("%Y-%m-%d %H:%M:%S")
    )

    print(
        f"Duration: {duration:.2f} seconds"
    )

    print("-" * 60)

    print(
        f"Total searches       : {len(SEARCHES) * 2}"
    )

    print(
        f"Successful searches  : {successful_searches}"
    )

    print(
        f"Failed searches      : {failed_searches}"
    )

    print(
        f"Total jobs received  : {total_received}"
    )

    print(
        f"Total new jobs saved : {total_saved}"
    )

    print(
        f"Total duplicates     : {total_duplicates}"
    )

    print("=" * 60)


# ==================================================
# Main
# ==================================================

if __name__ == "__main__":

    run_job_collection()