import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user_success():
    db = TestingSessionLocal()

    new_user = User(
        email="arsyid@example.com",
        hashed_password="1234123",
        full_name="Arsyid",
        phone_number="08123456789",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    assert new_user.id is not None
    assert new_user.email == "arsyid@example.com"
    assert new_user.hashed_password == "1234123"
    assert new_user.is_active == True
    assert new_user.is_admin == False
    assert new_user.full_name == "Arsyid"
    assert new_user.phone_number == "08123456789"
    db.close()

def test_create_user_duplicate_email_fails():
    db = TestingSessionLocal()

    first_user = User(
        email="arsyid@example.com",
        hashed_password="1234123",
        full_name="Arsyid",
        phone_number="0812345678",
    )
    db.add(first_user)
    db.commit()

    second_user = User(
        email="arsyid@example.com",
        hashed_password="1234123",
        full_name="Arsyid",
        phone_number="0812345678",
    )
    db.add(second_user)

    with pytest.raises(Exception):
        db.commit()

    db.rollback()
    db.close()