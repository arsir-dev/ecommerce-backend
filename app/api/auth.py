from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.models.models import User
from app.schemas.user import Token, UserLogin, UserResponse, UserCreate

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(path="/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    path="/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(credentials: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == credentials.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(credentials.password)

    new_user = User(
        email=credentials.email,
        hashed_password=hashed_password,
        full_name=str(credentials.full_name),
        phone_number=str(credentials.phone_number),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user