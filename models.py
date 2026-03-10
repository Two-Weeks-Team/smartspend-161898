import os
import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
    DateTime,
    Float,
    Numeric,
    ForeignKey,
    Text,
    Integer,
    func,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID as PGUUID

# ---------------------------------------------------------------------------
# Database connection handling (environment ‑ aware)
# ---------------------------------------------------------------------------

def _build_database_url() -> str:
    db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "sqlite:///./app.db"
    # Normalize URL schemes for psycopg driver
    if db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    elif db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
    return db_url

_DB_URL = _build_database_url()

# Determine SSL requirements – DigitalOcean managed Postgres requires SSL unless localhost
if not _DB_URL.startswith("sqlite") and "localhost" not in _DB_URL and "127.0.0.1" not in _DB_URL:
    _CONNECT_ARGS = {"sslmode": "require"}
else:
    _CONNECT_ARGS = {}

engine = create_engine(_DB_URL, connect_args=_CONNECT_ARGS, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ---------------------------------------------------------------------------
# Table name prefix (prevents collisions in shared DB)
# ---------------------------------------------------------------------------
_PREFIX = "ss_"

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = f"{_PREFIX}users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    health_scores = relationship("FinancialHealthScore", back_populates="user")

class Category(Base):
    __tablename__ = f"{_PREFIX}categories"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., 'income' or 'expense'
    is_custom = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")

class Transaction(Base):
    __tablename__ = f"{_PREFIX}transactions"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey(f"{_PREFIX}users.id"), nullable=False)
    institution_id = Column(PGUUID(as_uuid=True), nullable=True)  # simplified – no Institution model needed for demo
    date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(500))
    category_id = Column(PGUUID(as_uuid=True), ForeignKey(f"{_PREFIX}categories.id"), nullable=True)
    is_anomalous = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class Budget(Base):
    __tablename__ = f"{_PREFIX}budgets"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey(f"{_PREFIX}users.id"), nullable=False)
    category_id = Column(PGUUID(as_uuid=True), ForeignKey(f"{_PREFIX}categories.id"), nullable=True)
    monthly_limit = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")

class FinancialHealthScore(Base):
    __tablename__ = f"{_PREFIX}health_scores"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey(f"{_PREFIX}users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="health_scores")

# Create tables if they do not exist (useful for the demo environment)
Base.metadata.create_all(bind=engine)
