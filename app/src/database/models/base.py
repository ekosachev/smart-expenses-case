from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    id: Mapped[int]

    async def update(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)
