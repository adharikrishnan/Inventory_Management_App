import asyncio
from alembic.config import Config
from alembic import command
from database.database import AsyncSessionLocal
from sqlalchemy import select
from schema.user import User

mock_users: list[User] = [
    User(
        id=1,
        username="johndoe",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$4rLIRCKuyWfKObiTwtwPPQ$epg5LcSnfCD+W71z+1SGKN+dZ/Fb8IDNRcqcoM1mUP8",
        email="john.doe@example.com",
        first_name="John",
        last_name="Doe",
        disabled=False,
    ),
    User(
        id=2,
        username="janesmith",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$4rLIRCKuyWfKObiTwtwPPQ$epg5LcSnfCD+W71z+1SGKN+dZ/Fb8IDNRcqcoM1mUP8",
        email="jane.smith@example.com",
        first_name="Jane",
        last_name="Smith",
        disabled=False,
    ),
    User(
        id=3,
        username="alexm",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$4rLIRCKuyWfKObiTwtwPPQ$epg5LcSnfCD+W71z+1SGKN+dZ/Fb8IDNRcqcoM1mUP8",
        email=None,
        first_name="Alex",
        last_name="Morgan",
        disabled=True,
    ),
]

async def setup_database():
    await asyncio.to_thread(lambda: command.upgrade(Config("alembic.ini"), "head"))

# seed user data.
async def seed_mock_users() -> None:
    print("Seeding mock users...")
    async with AsyncSessionLocal() as session:
        existing = (await session.execute(select(User).limit(1))).fetchone()
        if not existing:
            session.add_all(mock_users)
            await session.commit()
            print("Mock users seeded successfully.")
        else:
            print("Mock users already exist in the database. Skipping seeding.")
# create tables and run migrations 
async def setup_local_database():
    await setup_database()
    await seed_mock_users()       
