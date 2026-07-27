import code

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.instrument_entity import (
    InstrumentEntity,
)

class InstrumentRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def get_by_code(
        self,
        code: str,
    ) -> InstrumentEntity | None:
        normalised_code = code.strip().upper()

        statement = select(
            InstrumentEntity
        ).where(
            InstrumentEntity.code
            == normalised_code
        )

        return self.session.scalar(
            statement
        )

    def list_active(
        self,
    ) -> list[InstrumentEntity]:
        statement = (
            select(InstrumentEntity)
            .where(
                InstrumentEntity.is_active
                .is_(True)
            )
            .order_by(
                InstrumentEntity.code
            )
        )

        return list(
            self.session.scalars(
                statement
            ).all()
        )

    def exists_by_code(
        self,
        code: str,
    ) -> bool:
        return self.get_by_code(
            code
        ) is not None
    
    def get_active_by_code(
        self,
        code: str,
    ) -> InstrumentEntity | None:
        normalised_code = code.strip().upper()

        statement = (
            select(InstrumentEntity)
            .where(
                InstrumentEntity.code
                == normalised_code,
                InstrumentEntity.is_active.is_(
                    True
                ),
            )
        )

        return self.session.scalar(
            statement
        )
        
    def exists_active_by_code(
        self,
        code: str,
    ) -> bool:
        return self.get_active_by_code(
            code
        ) is not None