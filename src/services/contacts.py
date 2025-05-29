from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas import ContactModel


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def get_contacts(self, skip: int = 0, limit: int = 10) -> list[ContactModel]:
        return await self.repository.get_contacts(skip, limit)

    async def get_contact_by_id(self, contact_id: int) -> ContactModel | None:
        return await self.repository.get_contact_by_id(contact_id)

    async def create_contact(self, contact: ContactModel) -> ContactModel:
        return await self.repository.create_contact(contact)

    async def update_contact(self, contact_id: int, contact: ContactModel) -> ContactModel | None:
        return await self.repository.update_contact(contact_id, contact)

    async def delete_contact(self, contact_id: int) -> ContactModel | None:
        return await self.repository.delete_contact(contact_id)

    async def search_contacts(self, query: str) -> list[ContactModel]:
        return await self.repository.search_contacts(query, self.repository.db)

    async def get_birthdays_in_next_days(self, days: int) -> list[ContactModel]:
        return await self.repository.get_birthdays(days, self.repository.db)
