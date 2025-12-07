#!/usr/bin/env python3
"""
make_sqlite.py

Create a SQLite database (file) with example tables and populate it with either:
 - CSV files found under data/raw/ (people.csv, transactions.csv), OR
 - a small synthetic dataset (default).

Usage:
  python make_sqlite.py              # creates db/example.db with synthetic data
  python make_sqlite.py --db db/foo.db
  python make_sqlite.py --force      # overwrite existing DB
"""

from pathlib import Path
import sqlite3
import csv
import argparse
from datetime import date, timedelta
import random
import sys

DEFAULT_DB = Path("db") / "example.db"
DATA_RAW = Path("data") / "raw"


def ensure_dirs(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)


def connect_db(db_path: Path, force: bool = False):
    if db_path.exists() and force:
        db_path.unlink()
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.executescript(
        """
    BEGIN;
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        age INTEGER
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        txn_date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (person_id) REFERENCES people (id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_transactions_person ON transactions (person_id);
    COMMIT;
    """
    )
    cur.close()


def insert_people(conn: sqlite3.Connection, people_rows):
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO people (id, name, email, age) VALUES (?, ?, ?, ?)",
        [(r["id"], r["name"], r.get("email"), r.get("age")) for r in people_rows],
    )
    conn.commit()


def insert_transactions(conn: sqlite3.Connection, txn_rows):
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO transactions (id, person_id, amount, txn_date, description) VALUES (?, ?, ?, ?, ?)",
        [(r["id"], r["person_id"], r["amount"], r["txn_date"], r.get("description")) for r in txn_rows],
    )
    conn.commit()


def load_csv_if_exists(conn: sqlite3.Connection):
    people_csv = DATA_RAW / "people.csv"
    tx_csv = DATA_RAW / "transactions.csv"
    loaded = False

    if people_csv.exists():
        with people_csv.open(newline="", encoding="utf8") as fh:
            reader = csv.DictReader(fh)
            rows = []
            for r in reader:
                # Expect columns: id,name,email,age
                rows.append(
                    {
                        "id": int(r["id"]),
                        "name": r.get("name"),
                        "email": r.get("email"),
                        "age": int(r["age"]) if r.get("age") else None,
                    }
                )
        insert_people(conn, rows)
        print(f"Loaded {len(rows)} people from {people_csv}")
        loaded = True

    if tx_csv.exists():
        with tx_csv.open(newline="", encoding="utf8") as fh:
            reader = csv.DictReader(fh)
            rows = []
            for r in reader:
                # Expect columns: id,person_id,amount,txn_date,description
                rows.append(
                    {
                        "id": int(r["id"]),
                        "person_id": int(r["person_id"]),
                        "amount": float(r["amount"]),
                        "txn_date": r["txn_date"],
                        "description": r.get("description"),
                    }
                )
        insert_transactions(conn, rows)
        print(f"Loaded {len(rows)} transactions from {tx_csv}")
        loaded = True

    return loaded


def generate_synthetic_data():
    # Small, deterministic-ish synthetic dataset
    people = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 35},
    ]

    # Create a handful of transactions across dates
    base = date(2020, 1, 1)
    txns = []
    tid = 1
    for person in people:
        # each person gets 3 transactions with small random amounts
        for i in range(3):
            txn_date = (base + timedelta(days=random.randint(0, 365))).isoformat()
            amount = round(random.uniform(-50.0, 200.0), 2)  # negative allowed (refunds)
            txns.append(
                {
                    "id": tid,
                    "person_id": person["id"],
                    "amount": amount,
                    "txn_date": txn_date,
                    "description": f"synthetic transaction {tid}",
                }
            )
            tid += 1

    return people, txns


def show_summary(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM people;")
    people_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM transactions;")
    txn_count = cur.fetchone()[0]
    print(f"Database summary: {people_count} people, {txn_count} transactions")
    print("\nSample people:")
    for row in cur.execute("SELECT id, name, email, age FROM people ORDER BY id LIMIT 5;"):
        print(row)
    print("\nSample transactions:")
    for row in cur.execute("SELECT id, person_id, amount, txn_date FROM transactions ORDER BY id LIMIT 5;"):
        print(row)
    cur.close()


def parse_args():
    p = argparse.ArgumentParser(description="Create example SQLite DB for course project.")
    p.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite file to create (default: db/example.db)")
    p.add_argument("--force", action="store_true", help="Overwrite existing DB file if present")
    return p.parse_args()


def main():
    args = parse_args()
    db_path: Path = args.db
    ensure_dirs(db_path)
    conn = connect_db(db_path, force=args.force)
    try:
        create_tables(conn)
        # Try to load CSVs in data/raw/, otherwise generate synthetic data
        loaded = load_csv_if_exists(conn)
        if not loaded:
            people, txns = generate_synthetic_data()
            insert_people(conn, people)
            insert_transactions(conn, txns)
            print(f"Inserted {len(people)} synthetic people and {len(txns)} synthetic transactions.")

        show_summary(conn)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        raise
    finally:
        conn.close()
        print(f"Database written to: {db_path}")


if __name__ == "__main__":
    main()