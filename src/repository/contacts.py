from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.database.models import Contact
from src.schemas import ContactModel


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int = 0, limit: int = 10) -> list[ContactModel]:
        query = select(Contact).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> ContactModel | None:
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, contact: ContactModel) -> ContactModel:
        result = Contact(**contact.model_dump(exclude_unset=True))
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update_contact(self, contact_id: int, contact: ContactModel) -> ContactModel | None:
        q_contact = await self.get_contact_by_id(contact_id)

        if q_contact:
            q_contact.name = contact.name
            q_contact.last_name = contact.last_name
            q_contact.email = contact.email
            q_contact.phone = contact.phone
            q_contact.birthday = contact.birthday
            await self.db.commit()
            await self.db.refresh(q_contact)

        return q_contact

    async def delete_contact(self, contact_id: int) -> ContactModel | None:
        q_contact = await self.get_contact_by_id(contact_id)

        if q_contact:
            await self.db.delete(q_contact)
            await self.db.commit()

        return q_contact

    async def search_contacts(self, query: str) -> list[ContactModel]:
        stmt = select(Contact).filter(
            (Contact.name.ilike(f"%{query}%")) |
            (Contact.last_name.ilike(f"%{query}%")) |
            (Contact.email.ilike(f"%{query}%"))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_birthdays(self, days: int) -> list[ContactModel]:
        today = datetime.today()
        end = today + timedelta(days=days)
        stmt = select(Contact).filter(
            func.extract("month", Contact.birthday) == today.month,
            func.extract("day", Contact.birthday) >= today.day,
            func.extract("day", Contact.birthday) <= end.day
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contacts_count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Contact))
        return result.scalar_one()
