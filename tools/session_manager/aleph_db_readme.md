# aleph.db — SQLite Session Database

SQLite database persisting session state across runs.
Contains: battery results, sigma events, findings, session metadata.

This file is tracked in git for completeness.
To inspect: `sqlite3 aleph.db .tables` then `SELECT * FROM table_name;`
