from beanie import Document
from beanie import init_beanie
import asyncio
from pymongo import AsyncMongoClient
import base64
from pydantic import BaseModel
from beanie.operators import In, Set

class Category(BaseModel):
    type: str
    description: str
    format: str = None
    socket: str = None
    frequency: str = None
    volume: str = None
    form_factor: str = None
    ports: list = None

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

    components = [
        PC_components(Production="ASUS", Model="ROG STRIX Z790-E", Price=450.0, category=Category(type="материнская плата", description="Игровая", format="ATX", socket="LGA1700")),
        PC_components(Production="MSI", Model="MAG B550 TOMAHAWK", Price=140.0, category=Category(type="материнская плата", description="Для AMD", format="ATX", socket="AM4")),
        PC_components(Production="Gigabyte", Model="B760M DS3H", Price=110.0, category=Category(type="материнская плата", description="Бюджетная", format="Micro-ATX", socket="LGA1700")),
        PC_components(Production="ASRock", Model="X570 Taichi", Price=300.0, category=Category(type="материнская плата", description="Премиум", format="ATX", socket="AM4")),
        PC_components(Production="ASUS", Model="PRIME H610M-K", Price=80.0, category=Category(type="материнская плата", description="Офисная", format="Micro-ATX", socket="LGA1700")),
        PC_components(Production="ASUS", Model="TUF GAMING B450-PLUS II", Price=100.0, category=Category(type="материнская плата", description="Базовая AMD", format="ATX", socket="AM4")),

        PC_components(Production="Intel", Model="Core i9-14900K", Price=580.0, category=Category(type="процессор", description="Флагман", socket="LGA1700", frequency="3.2 GHz")),
        PC_components(Production="AMD", Model="Ryzen 7 5800X3D", Price=300.0, category=Category(type="процессор", description="Игровой", socket="AM4", frequency="3.4 GHz")),
        PC_components(Production="Intel", Model="Core i5-14600K", Price=320.0, category=Category(type="процессор", description="Оптимальный", socket="LGA1700", frequency="3.5 GHz")),
        PC_components(Production="AMD", Model="Ryzen 5 5600X", Price=150.0, category=Category(type="процессор", description="Народный", socket="AM4", frequency="3.7 GHz")),
        PC_components(Production="Intel", Model="Core i3-14100", Price=115.0, category=Category(type="процессор", description="Бюджетный", socket="LGA1700", frequency="3.5 GHz")),
        PC_components(Production="AMD", Model="Ryzen 9 5950X", Price=400.0, category=Category(type="процессор", description="Для работы", socket="AM4", frequency="3.4 GHz")),

        PC_components(Production="Corsair", Model="Vengeance LPX", Price=80.0, category=Category(type="ОЗУ", description="Низкопрофильная", frequency="3200 MHz", volume="32 GB")),
        PC_components(Production="Kingston", Model="Fury Beast", Price=70.0, category=Category(type="ОЗУ", description="Надежная", frequency="3200 MHz", volume="32 GB")),
        PC_components(Production="G.Skill", Model="Trident Z Neo", Price=110.0, category=Category(type="ОЗУ", description="Разгон", frequency="3600 MHz", volume="32 GB")),
        PC_components(Production="Crucial", Model="Basics", Price=35.0, category=Category(type="ОЗУ", description="Простая", frequency="2666 MHz", volume="8 GB")),
        PC_components(Production="TeamGroup", Model="T-Force Delta RGB", Price=65.0, category=Category(type="ОЗУ", description="Игровая", frequency="3600 MHz", volume="16 GB")),
        PC_components(Production="Patriot", Model="Viper Steel", Price=95.0, category=Category(type="ОЗУ", description="Быстрая", frequency="4000 MHz", volume="32 GB")),

        PC_components(Production="Samsung", Model="990 PRO", Price=170.0, category=Category(type="ПЗУ", description="Быстрый NVMe", form_factor="M.2 2280", volume="2 TB")),
        PC_components(Production="WD", Model="Black SN850X", Price=150.0, category=Category(type="ПЗУ", description="Игровой SSD", form_factor="M.2 2280", volume="2 TB")),
        PC_components(Production="Crucial", Model="MX500", Price=65.0, category=Category(type="ПЗУ", description="SATA SSD", form_factor="2.5 inch", volume="1 TB")),
        PC_components(Production="Kingston", Model="NV2", Price=60.0, category=Category(type="ПЗУ", description="Бюджетный NVMe", form_factor="M.2 2280", volume="1 TB")),
        PC_components(Production="Seagate", Model="BarraCuda", Price=55.0, category=Category(type="ПЗУ", description="Жесткий диск", form_factor="3.5 inch", volume="2 TB")),
        PC_components(Production="WD", Model="Blue SA510", Price=40.0, category=Category(type="ПЗУ", description="Обычный SSD", form_factor="2.5 inch", volume="500 GB")),

        PC_components(Production="NVIDIA", Model="RTX 4090", Price=2000.0, category=Category(type="видеокарта", description="Топ графика", volume="24 GB", ports=["HDMI", "DisplayPort"])),
        PC_components(Production="ASUS", Model="TUF RX 7800 XT", Price=550.0, category=Category(type="видеокарта", description="Radeon", volume="16 GB", ports=["HDMI", "DisplayPort"])),
        PC_components(Production="MSI", Model="RTX 4070 Ti SUPER", Price=850.0, category=Category(type="видеокарта", description="Для 2K", volume="16 GB", ports=["HDMI", "DisplayPort"])),
        PC_components(Production="Gigabyte", Model="RTX 4060", Price=300.0, category=Category(type="видеокарта", description="Народная", volume="8 GB", ports=["HDMI", "DisplayPort"])),
        PC_components(Production="Sapphire", Model="Pulse RX 7600", Price=270.0, category=Category(type="видеокарта", description="Входной билет", volume="8 GB", ports=["HDMI", "DisplayPort"])),
        PC_components(Production="Palit", Model="RTX 4080 SUPER", Price=1100.0, category=Category(type="видеокарта", description="Мощная", volume="16 GB", ports=["HDMI", "DisplayPort"]))
    ]

    await PC_components.insert_many(components)

if __name__ == "__main__":
    asyncio.run(main())