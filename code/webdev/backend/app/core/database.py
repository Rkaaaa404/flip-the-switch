from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create tables and automatically apply schema updates (missing columns) for SQLite/DB."""
    Base.metadata.create_all(bind=engine)
    try:
        inspector = inspect(engine)
        with engine.connect() as conn:
            for table_name, table in Base.metadata.tables.items():
                if inspector.has_table(table_name):
                    existing_cols = {c["name"] for c in inspector.get_columns(table_name)}
                    for column in table.columns:
                        if column.name not in existing_cols:
                            col_type = column.type.compile(engine.dialect)
                            sql = f"ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type}"
                            conn.execute(text(sql))
                            conn.commit()
                            print(f"📦 DB Migration: Added column '{column.name}' ({col_type}) to table '{table_name}'")
    except Exception as e:
        print(f"⚠️ DB Migration warning: {e}")