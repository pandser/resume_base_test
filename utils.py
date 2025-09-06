import bcrypt
import jwt

from settings import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ) -> str:
    '''Генерация токена.'''
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        jwt_token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ):
    '''Декодирование токена.'''
    decoded = jwt.decode(
        jwt=jwt_token,
        key=public_key,
        algorithms=[algorithm],
        options={                # исправляет ошибку
            "verify_sub": False, # jwt.exceptions.InvalidSubjectError: Subject must be a string
        }
    )
    return decoded


def hash_password(password: str) -> bytes:
    '''Хэширование пароля для сохранения в БД.'''
    return bcrypt.hashpw(
        password=password.encode('utf-8'),
        salt=bcrypt.gensalt(),
    )


def check_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
    '''Проверка корректности пароля.'''
    return bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=hashed_password,
    )
