from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError

from utils import decode_jwt
from database import db_helper
from models import ResumesModel, UsersModel
from schemas import (
    ResumesGetSchema,
    ResumesAddSchema,
    ResumesOptionalSchema,
    UsersGetSchema,
)


router = APIRouter(
    prefix='/resume',
    tags=['резюме'],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    '''Получение информации о пользователе из текущего токена.'''
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token',
        )
    return payload


async def get_current_user(
    payload: dict = Depends(get_current_token_payload),
) -> UsersGetSchema:
    '''Получение текущего пользователя.'''
    user_id = payload.get('sub')
    async with db_helper.session_factory() as session:
        user = await session.get(UsersModel, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Не верный токен',
            )
        return UsersGetSchema(
            user_id=user.id,
            usesrname=user.username,
            email=user.email,
        )


@router.get(
    '/',
    summary='Получение всех резюме пользователя.'
)
async def get_resume(
    user: UsersGetSchema = Depends(get_current_user),
) -> list[ResumesGetSchema]:
    '''Возвращает список всех резюме текущего пользователя.'''
    result = await db_helper.get_resumes_user(user=user)
    return [
        ResumesGetSchema.model_validate(row, from_attributes=True)
        for row in result.scalars().all()
    ]


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Добавление резюме'
)
async def create_resume(
    data: ResumesAddSchema,
    user: UsersGetSchema = Depends(get_current_user),
):
    '''Добавление резюме для текущего пользователя.'''
    result =  await db_helper.create_resume_in_db(
        data=data,
        user=user,
    )
    return result


@router.patch(
    '/{resume_id}',
    status_code=status.HTTP_202_ACCEPTED,
    summary='Редактирование резюме'
)
async def update_resume(
    resume_id: int,
    data: ResumesOptionalSchema,
    user: UsersGetSchema = Depends(get_current_user),
):
    '''Редактирование резюме'''
    result = await db_helper.update_resume_in_db(
        resume_id=resume_id,
        data=data,
        user=user,
    )
    return result


@router.delete(
    '/{resume_id}',
    status_code=status.HTTP_202_ACCEPTED,
    summary='Удаление резюме'
)
async def update_resume(
    resume_id: int,
    user: UsersGetSchema = Depends(get_current_user),
):
    '''Удаление резюме.'''
    result = await db_helper.del_resume_from_db(
        resume_id=resume_id,
        user=user,
    )
    return result


@router.get(
    '/{resume_id}/improve',
    summary='Интеграция с AI(заглушка)'    
)
async def ai_update_resume(
    response: Response,
    resume_id: int,
    user: UsersGetSchema = Depends(get_current_user),
):
    '''Принимает текст резюме и возвращает текст + [improved].'''
    resume: ResumesModel = await db_helper.get_resume(resume_id=resume_id)
    if resume.user_id != user.user_id:
        response.status_code = status.HTTP_403_FORBIDDEN
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Доступ запрещен'
        )
    result = resume.content + ' [improved]'
    return {'content': result}
