python
import asyncio
import aiohttp
import asyncpg
import re
from db import insert_characters, create_tables

async def get_person_data(session, person_id):
    try:
        async with session.get(f'https://www.swapi.tech/api/people/{person_id}') as response:
            if response.status == 200:
                data = await response.json()
                props = data['result']['properties']
                
                homeworld_url = props['homeworld']
                homeworld_match = re.search(r'planets/(\d+)', homeworld_url)
                homeworld_id = int(homeworld_match.group(1)) if homeworld_match else None
                
                try:
                    mass = float(props['mass']) if props['mass'] not in ['unknown', 'none'] else None
                except (ValueError, TypeError):
                    mass = None
                
                return {
                    'id': person_id,
                    'birth_year': props.get('birth_year', 'unknown'),
                    'eye_color': props.get('eye_color', 'unknown'),
                    'gender': props.get('gender', 'unknown'),
                    'hair_color': props.get('hair_color', 'unknown'),
                    'homeworld': homeworld_id,
                    'mass': mass,
                    'name': props['name'],
                    'skin_color': props.get('skin_color', 'unknown')
                }
            else:
                print(f"Ошибка для персонажа {person_id}: {response.status}")
                return None
    except Exception as e:
        print(f"Исключение для персонажа {person_id}: {e}")
        return None

async def main():
    await create_tables()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for person_id in range(1, 100):  # Примерный диапазон ID
            task = asyncio.create_task(get_person_data(session, person_id))
            tasks.append(task)
        
        characters_data = await asyncio.gather(*tasks)
        
        valid_characters = [char for char in characters_data if char is not None]
        
        character_tuples = [
            (char['id'], char['birth_year'], char['eye_color'], char['gender'],
             char['hair_color'], char['homeworld'], char['mass'], 
             char['name'], char['skin_color'])
            for char in valid_characters
        ]
        
        await insert_characters(character_tuples)
        print(f"Успешно загружено {len(valid_characters)} персонажей")

if __name__ == '__main__':
    asyncio.run(main())
