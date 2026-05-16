import asyncio
import base64
from beanie import Document, init_beanie
from pymongo import AsyncMongoClient  

class Avatars(Document):
    name: str
    file: bytes

    class Settings:
        name = "avatars"

def file_to_base64_str(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        encoding_string = base64.b64encode(file.read())
    return encoding_string

def base64_str_to_file(base64_string: bytes, output_path: str):
    with open(output_path, "wb") as file:
        decode_data = base64.b64decode(base64_string)
        file.write(decode_data)

async def avatars_main():
    client = AsyncMongoClient("mongodb://localhost:27017/")
    db = client.AVATARS

    await init_beanie(database=db, document_models=[Avatars])

    try:
        avatar_file = Avatars(
            name="image.png",
            file=file_to_base64_str("image.png"),
        )
        await avatar_file.insert()
        print("Аватар сохранен")
    except FileNotFoundError:
        print("Файл image.png не найден в папке со скриптом")

if __name__ == "__main__":
    asyncio.run(avatars_main())