from beanie import Document
from beanie import init_beanie
import asyncio
from pymongo import AsyncMongoClient
import base64
from pydantic import BaseModel
from beanie.operators import In, Set
from typing import Optional

class Category(BaseModel):
    type: str
    description: str
    format: Optional[str] = None
    socket: Optional[str] = None
    frequency: Optional[str] = None
    volume: Optional[str] = None
    form_factor: Optional[str] = None
    ports: Optional[list] = None

class PC_components(Document):
    Production: str #(производитель)
    Model: str #(модель)
    Price: float #(цена)
    category: Category

    class Settings:
        name = "PC_components" # Имя коллекции

async def main():
    # Подключение
    client = AsyncMongoClient("mongodb://localhost:27017/")
    db = client.Catalog

    # Инициализация Beanie с моделями
    await init_beanie(database=db, document_models=[PC_components])

    print("=== 1. САМАЯ ДЕШЕВАЯ И САМАЯ ДОРОГАЯ СБОРКА ===")
    
    cheap_ram = await PC_components.find({"category.type": "ОЗУ"}).sort("+Price").first_or_none()
    cheap_storage = await PC_components.find({"category.type": "ПЗУ"}).sort("+Price").first_or_none()
    cheap_videocard = await PC_components.find({"category.type": "видеокарта"}).sort("+Price").first_or_none()

    expensive_ram = await PC_components.find({"category.type": "ОЗУ"}).sort("-Price").first_or_none()
    expensive_storage = await PC_components.find({"category.type": "ПЗУ"}).sort("-Price").first_or_none()
    expensive_videocard = await PC_components.find({"category.type": "видеокарта"}).sort("-Price").first_or_none()

    cheap_am4_motherboard = await PC_components.find({"category.type": "материнская плата", "category.socket": "AM4"}).sort("+Price").first_or_none()
    cheap_am4_processor = await PC_components.find({"category.type": "процессор", "category.socket": "AM4"}).sort("+Price").first_or_none()
    
    cheap_lga_motherboard = await PC_components.find({"category.type": "материнская плата", "category.socket": "LGA1700"}).sort("+Price").first_or_none()
    cheap_lga_processor = await PC_components.find({"category.type": "процессор", "category.socket": "LGA1700"}).sort("+Price").first_or_none()

    am4_cheap_pair_price = cheap_am4_motherboard.Price + cheap_am4_processor.Price
    lga_cheap_pair_price = cheap_lga_motherboard.Price + cheap_lga_processor.Price

    if am4_cheap_pair_price < lga_cheap_pair_price:
        final_cheap_motherboard = cheap_am4_motherboard
        final_cheap_processor = cheap_am4_processor
    else:
        final_cheap_motherboard = cheap_lga_motherboard
        final_cheap_processor = cheap_lga_processor

    expensive_am4_motherboard = await PC_components.find({"category.type": "материнская плата", "category.socket": "AM4"}).sort("-Price").first_or_none()
    expensive_am4_processor = await PC_components.find({"category.type": "процессор", "category.socket": "AM4"}).sort("-Price").first_or_none()
    
    expensive_lga_motherboard = await PC_components.find({"category.type": "материнская плата", "category.socket": "LGA1700"}).sort("-Price").first_or_none()
    expensive_lga_processor = await PC_components.find({"category.type": "процессор", "category.socket": "LGA1700"}).sort("-Price").first_or_none()

    am4_expensive_pair_price = expensive_am4_motherboard.Price + expensive_am4_processor.Price
    lga_expensive_pair_price = expensive_lga_motherboard.Price + expensive_lga_processor.Price

    if am4_expensive_pair_price > lga_expensive_pair_price:
        final_expensive_motherboard = expensive_am4_motherboard
        final_expensive_processor = expensive_am4_processor
    else:
        final_expensive_motherboard = expensive_lga_motherboard
        final_expensive_processor = expensive_lga_processor

    total_cheap_price = final_cheap_motherboard.Price + final_cheap_processor.Price + cheap_ram.Price + cheap_storage.Price + cheap_videocard.Price
    total_expensive_price = final_expensive_motherboard.Price + final_expensive_processor.Price + expensive_ram.Price + expensive_storage.Price + expensive_videocard.Price

    print(f"Дешевая сборка ({final_cheap_motherboard.category.socket}): {final_cheap_motherboard.Model} + {final_cheap_processor.Model} + {cheap_ram.Model} + {cheap_storage.Model} + {cheap_videocard.Model}")
    print(f"Цена: {total_cheap_price} $")
    print(f"Дорогая сборка ({final_expensive_motherboard.category.socket}): {final_expensive_motherboard.Model} + {final_expensive_processor.Model} + {expensive_ram.Model} + {expensive_storage.Model} + {expensive_videocard.Model}")
    print(f"Цена: {total_expensive_price} $")
    print("-" * 50)


    print("=== 2. ТРЕТИЙ И ПЯТЫЙ ПО СТОИМОСТИ ТТОВАРЫ ===")
    pipeline = [
        {"$sort": {"Price": -1}},
        {
            "$group": {
                "_id": "$category.type",
                "products": {
                    "$push": {
                        "Production": "$Production",
                        "Model": "$Model",
                        "Price": "$Price"
                    }
                }
            }
        },
        {
            "$project": {
                "category": "$_id",
                "third": {"$arrayElemAt": ["$products", 2]},
                "fifth": {"$arrayElemAt": ["$products", 4]}
            }
        }
    ]

    aggregation_results = await PC_components.aggregate(pipeline).to_list()

    for item in aggregation_results:
        print(f"Категория: {item['category']}")
        if item.get("third"):
            print(f"  3-й по стоимости: {item['third']['Production']} {item['third']['Model']} — {item['third']['Price']}")
        if item.get("fifth"):
            print(f"  5-й по стоимости: {item['fifth']['Production']} {item['fifth']['Model']} — {item['fifth']['Price']}")
        print("-" * 40)


    print("=== 3. ВСЕ ВОЗМОЖНЫЕ СБОРКИ НА СОКЕТЕ АМ4 ===")

    am4_motherboards = await PC_components.find({"category.type": "материнская плата", "category.socket": "AM4"}).to_list()
    am4_processors = await PC_components.find({"category.type": "процессор", "category.socket": "AM4"}).to_list()
    all_rams = await PC_components.find({"category.type": "ОЗУ"}).to_list()
    all_storages = await PC_components.find({"category.type": "ПЗУ"}).to_list()
    all_videocards = await PC_components.find({"category.type": "видеокарта"}).to_list()

    build_counter = 0
    
    with open("am4_builds.txt", "w", encoding="utf-8") as file:
        file.write("СПИСОК ВСЕХ ВОЗМОЖНЫХ СБОРОК НА СОКЕТЕ AM4\n")
        file.write("=" * 60 + "\n\n")
        
        for motherboard in am4_motherboards:
            for processor in am4_processors:
                for ram in all_rams:
                    for storage in all_storages:
                        for videocard in all_videocards:
                            build_counter += 1
                            build_total_price = motherboard.Price + processor.Price + ram.Price + storage.Price + videocard.Price
                            
                            file.write(f"Сборка №{build_counter}: {motherboard.Model} + {processor.Model} + {ram.Model} + {storage.Model} + {videocard.Model} = {build_total_price} $\n")

    print(f"Успешно сгенерировано {build_counter} сборок!")
    print("Все варианты сохранены в файл: am4_builds.txt")

if __name__ == "__main__":
    asyncio.run(main())