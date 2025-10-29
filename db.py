import asyncpg
import asyncio

async def create_tables():
    conn = await asyncpg.connect('postgresql://user:password@localhost/db')
    
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS characters(
            id INTEGER PRIMARY KEY,
            birth_year VARCHAR(20),
            eye_color VARCHAR(20),
            gender VARCHAR(20),
            hair_color VARCHAR(20),
            homeworld INTEGER,
            mass NUMERIC,
            name VARCHAR(100) NOT NULL,
            skin_color VARCHAR(50)
        )
    ''')
    await conn.close()

async def insert_characters(character_data):
    conn = await asyncpg.connect('postgresql://user:password@localhost/db')
    
    await conn.executemany('''
        INSERT INTO characters (id, birth_year, eye_color, gender, hair_color, homeworld, mass, name, skin_color)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (id) DO UPDATE SET
            birth_year = EXCLUDED.birth_year,
            eye_color = EXCLUDED.eye_color,
            gender = EXCLUDED.gender,
            hair_color = EXCLUDED.hair_color,
            homeworld = EXCLUDED.homeworld,
            mass = EXCLUDED.mass,
            name = EXCLUDED.name,
            skin_color = EXCLUDED.skin_color
    ''', character_data)
    
    await conn.close()
