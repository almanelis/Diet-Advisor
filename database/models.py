from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Декларативный класс модели ДБ
class Base(DeclarativeBase):
    ...


# Модель пользователя
class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True ,nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    profile: Mapped['Profile'] = relationship(back_populates='user')


# Модель профиля пользователя со связью OneToOne
class Profile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(5), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='profile')
    