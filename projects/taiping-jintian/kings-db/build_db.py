import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORDS = HERE / "records.json"
DB = HERE / "taiping-kings.db"

rows = json.loads(RECORDS.read_text(encoding="utf-8"))

if DB.exists():
    DB.unlink()

con = sqlite3.connect(DB)
con.execute(
    """
    CREATE TABLE kings (
        id INTEGER PRIMARY KEY,
        title TEXT,
        name TEXT,
        honorific TEXT,
        full_title TEXT,
        birth TEXT,
        death TEXT,
        death_place TEXT,
        achievement TEXT,
        source TEXT,
        portrait_url TEXT,
        portrait_note TEXT,
        note TEXT
    )
    """
)
con.executemany(
    """
    INSERT INTO kings (id, title, name, honorific, full_title, birth, death,
                       death_place, achievement, source, portrait_url,
                       portrait_note, note)
    VALUES (:id, :title, :name, :honorific, :full_title, :birth, :death,
            :death_place, :achievement, :source, :portrait_url,
            :portrait_note, :note)
    """,
    rows,
)
con.commit()

print(f"built {DB.name} with {con.execute('SELECT COUNT(*) FROM kings').fetchone()[0]} rows")
for r in con.execute("SELECT id, title, name, birth, death FROM kings"):
    print(r)
con.close()
