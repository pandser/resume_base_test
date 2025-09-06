from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from utils import hash_password
from models import ResumesModel, UsersModel
from settings import settings
from schemas import (
    ResumesAddSchema,
    ResumesOptionalSchema,
    UsersGetSchema,
    UsersInDBSchema,
)


class DatabaseHelper:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def create_user_in_db(
        self,
        data: UsersInDBSchema,
        session: AsyncSession,
    ) -> None:
        '''Добавление пользователя в БД.'''
        try:
            user = UsersModel(
                username=data.usesrname,
                email=data.email,
                hashed_password=hash_password(password=data.password),
            )
            session.add(user)
            await session.commit()
        except IntegrityError as e:
            raise Exception()
        return user

    async def get_user_from_db(
        self,
        username: str,
    ):
        '''Получение пользователя из БД.'''
        query = (
            select(UsersModel)
            .filter_by(username=username)
        )
        async with self.session_factory() as session:
            res = await session.execute(query)
            user = res.scalar()
        return user
    
    async def get_resumes_user(
        self,
        user: UsersGetSchema,
    ) -> ResumesModel:
        '''Получение всех резюме пользователя из БД.'''
        query = (
            select(ResumesModel)
            .filter(ResumesModel.user_id == user.user_id)
        )
        async with self.session_factory() as session:
            result = await session.execute(query)
        return result
    
    async def create_resume_in_db(
        self,
        data: ResumesAddSchema,
        user: UsersGetSchema,
    ):
        '''Добавление резюме в БД.'''
        resume = ResumesModel(
            title=data.title,
            content=data.content,
            user_id=user.user_id
        )
        async with self.session_factory() as session:
            session.add(resume)
            await session.commit()
        return {'message': 'резюме добавлено'}

    async def get_resume(
        self,
        resume_id: int,
    ) -> ResumesModel:
        '''Получение резюме из БД по id.'''
        async with self.session_factory() as session:
            resume: ResumesModel = await session.get(ResumesModel, resume_id)
        return resume

    async def update_resume_in_db(
        self,
        resume_id: int,
        data: ResumesOptionalSchema,
        user: UsersGetSchema,
    ):
        '''Обновление резюме в БД.'''
        content = data.content
        title = data.title
        async with self.session_factory() as session:
            resume: ResumesModel = await session.get(ResumesModel, resume_id)
            if not resume:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if user.user_id != resume.user_id:
                return HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Доступ запрещен'
                )
            if content and title:
                resume.content = content
                resume.title = title
            elif content:
                resume.content = content
            else:
                resume.title = title
            await session.commit()
        return {'message': 'Резюме обновлено'}
    
    async def del_resume_from_db(
            self,
            resume_id: int,
            user: UsersGetSchema,
    ):
        '''Удаление резюме из БД.'''
        async with self.session_factory() as session:
            resume: ResumesModel = await session.get(ResumesModel, resume_id)
            if not resume:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if user.user_id != resume.user_id:
                return HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Доступ запрещен'
                )
            await session.delete(resume)
            await session.commit()
        return {'message': 'Резюме удалено'}


db_helper = DatabaseHelper(
    url=settings.db_url,
)
