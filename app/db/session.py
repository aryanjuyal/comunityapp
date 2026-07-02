from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()

    try:
        yield db  # Runs until yield unlike return which runs once and exits the functionand db session closes instantly. Yield allows the function to be paused and resumed, keeping the db session open for the duration of the request.

    finally:
        db.close()

        # db.commit() what iit does is it starts a transactionand send the pending SQL statements to postgreSQL
        # a transaction is a sequence of operations performed as a single logical unit of work. A transaction has four properties, known as the ACID properties: Atomicity, Consistency, Isolation, and Durability.
        # amd a transaction is a way we use to commit everything or nothing at all. If any of the operations fail, the entire transaction is rolled back, and no changes are made to the database. This ensures that the database remains in a consistent state even in the event of an error or failure.