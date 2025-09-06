from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from utils import encode_jwt, check_password
from database import db_helper
from models import UsersModel
from settings import settings
from schemas import UsersInDBSchema, TokenSchema


router = APIRouter(
    prefix='/auth',
    tags=['аутентификация'],
)


async def authenticate_user(username: str, password: str):
    user = await db_helper.get_user_from_db(
        username=username,
    )
    if not user:
        return False
    if not check_password(password, user.hashed_password):
        return False
    return user


@router.post(
    '/sign_up',
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация пользователя'
)
async def create_user(data: UsersInDBSchema):
    '''Регистрация нового пользователя в системе.'''
    async with db_helper.session_factory() as session:
        try: 
            user: UsersModel = await db_helper.create_user_in_db(
                data=data,
                session=session,
            )
        except Exception:
            return {'message': 'Пользователь уже существует.'}
    return {'message': f'user {user.username} created'}


@router.post(
    "/token",
    summary='Получение токена'
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    '''Получение JWT-токена для пользователя.'''
    user: UsersModel = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    time_now = datetime.now(timezone.utc)
    delta = timedelta(
        minutes=settings.auth_jwt.access_token_expires_minutes,
    )
    access_token_expires = time_now + delta
    jwt_payload = {
        'sub': user.id,
        'email': user.email,
        'iat': time_now,
        'exp': access_token_expires, 
    }
    access_token = encode_jwt(
        payload=jwt_payload,
    )
    return TokenSchema(access_token=access_token, token_type="Bearer")
