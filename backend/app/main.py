from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import db
from app.middleware.cors import setup_cors
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed data if needed
    if await db.products.count_documents({}) == 0:
        demo_products = [
            {"name": "Vestido de Seda Minimal", "category": "Vestidos", "price": "€1,200", "img": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80"},
            {"name": "Blusa de Lino Blanco", "category": "Blusas", "price": "€450", "img": "https://images.unsplash.com/photo-1551163943-3f6a855d1153?w=800&q=80"},
            {"name": "Pantalón Sastre Negro", "category": "Pantalones", "price": "€800", "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&q=80"},
            {"name": "Chaqueta de Cuero Premium", "category": "Chaquetas", "price": "€2,500", "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80"},
            {"name": "Stilettos Clásicos", "category": "Zapatos", "price": "€750", "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&q=80"},
            {"name": "Bolso de Mano Estructurado", "category": "Bolsos", "price": "€3,200", "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&q=80"},
        ]
        await db.products.insert_many(demo_products)

    if await db.saved_looks.count_documents({}) == 0:
        demo_looks = [
            {"name": "Business Luxury", "img": "https://images.unsplash.com/photo-1485230895905-ec17bd368582?w=800&q=80"},
            {"name": "Gala Night", "img": "https://images.unsplash.com/photo-1539109132314-3477524c8959?w=800&q=80"},
            {"name": "Summer Riviera", "img": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=800&q=80"},
        ]
        await db.saved_looks.insert_many(demo_looks)

    if await db.fashion_links.count_documents({}) == 0:
        demo_links = [
            {"name": "Pinterest", "url": "https://pinterest.com", "img": "https://logo.clearbit.com/pinterest.com", "category": "Inspiración", "favorite": True},
            {"name": "Vogue", "url": "https://vogue.com", "img": "https://logo.clearbit.com/vogue.com", "category": "Inspiración", "favorite": True},
            {"name": "Farfetch", "url": "https://farfetch.com", "img": "https://logo.clearbit.com/farfetch.com", "category": "Tienda", "favorite": False},
            {"name": "Zara", "url": "https://zara.com", "img": "https://logo.clearbit.com/zara.com", "category": "Tienda", "favorite": False},
        ]
        await db.fashion_links.insert_many(demo_links)

    yield


app = FastAPI(title="Fashion Key API", version="1.0.0", lifespan=lifespan)
setup_cors(app)
app.include_router(auth.router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
