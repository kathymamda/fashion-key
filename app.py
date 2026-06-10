import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = "fashion_key_secret_key"

# Configuración MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "fashion_key")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    # Verificar conexión
    client.server_info()
    print("----------------------------------------")
    print("MONGODB: Conectado correctamente")
    print("----------------------------------------")
except Exception as e:
    print("----------------------------------------")
    print(f"MONGODB ERROR: {e}")
    print("----------------------------------------")

# Colecciones
users_col = db['users']
body_profiles_col = db['body_profiles']
saved_looks_col = db['saved_looks']
recommendations_col = db['recommendations']
fashion_links_col = db['fashion_links']
favorite_items_col = db['favorite_items']
products_col = db['products']

# Seeding de datos si están vacíos
def seed_data():
    if products_col.count_documents({}) == 0:
        demo_products = [
            {"name": "Vestido de Seda Minimal", "category": "Vestidos", "price": "€1,200", "img": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80"},
            {"name": "Blusa de Lino Blanca", "category": "Blusas", "price": "€450", "img": "https://images.unsplash.com/photo-1551163943-3f6a855d1153?w=800&q=80"},
            {"name": "Pantalón Sastre Negro", "category": "Pantalones", "price": "€800", "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&q=80"},
            {"name": "Chaqueta de Cuero Premium", "category": "Chaquetas", "price": "€2,500", "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80"},
            {"name": "Stilettos Clásicos", "category": "Zapatos", "price": "€750", "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&q=80"},
            {"name": "Bolso de Mano Estructurado", "category": "Bolsos", "price": "€3,200", "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&q=80"}
        ]
        # Añadir más hasta 20
        for i in range(7, 21):
            demo_products.append({
                "name": f"Prenda Editorial {i}",
                "category": "Moda",
                "price": f"€{i*150}",
                "img": f"https://images.unsplash.com/photo-{1500000000000 + i}?w=800&q=80"
            })
        products_col.insert_many(demo_products)

    if saved_looks_col.count_documents({}) == 0:
        demo_looks = [
            {"name": "Business Luxury", "img": "https://images.unsplash.com/photo-1485230895905-ec17bd368582?w=800&q=80"},
            {"name": "Gala Night", "img": "https://images.unsplash.com/photo-1539109132314-3477524c8959?w=800&q=80"},
            {"name": "Summer Riviera", "img": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=800&q=80"}
        ]
        saved_looks_col.insert_many(demo_looks)

    if fashion_links_col.count_documents({}) == 0:
        demo_links = [
            {"name": "Pinterest", "url": "https://pinterest.com", "img": "https://logo.clearbit.com/pinterest.com", "category": "Inspiración", "favorite": True},
            {"name": "Vogue", "url": "https://vogue.com", "img": "https://logo.clearbit.com/vogue.com", "category": "Inspiración", "favorite": True},
            {"name": "Farfetch", "url": "https://farfetch.com", "img": "https://logo.clearbit.com/farfetch.com", "category": "Tienda", "favorite": False},
            {"name": "Zara", "url": "https://zara.com", "img": "https://logo.clearbit.com/zara.com", "category": "Tienda", "favorite": False}
        ]
        fashion_links_col.insert_many(demo_links)

seed_data()

# Rutas
@app.route('/')
def index():
    products = list(products_col.find().limit(12))
    outfits = list(saved_looks_col.find().limit(5))
    return render_template('index.html', products=products, outfits=outfits)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    products = list(products_col.find().limit(6))
    return render_template('dashboard.html', section='main', products=products)

@app.route('/body-analysis')
def body_analysis():
    return render_template('body-analysis.html', section='body')

@app.route('/simulator')
def simulator():
    products = list(products_col.find())
    return render_template('simulator.html', products=products)

@app.route('/inspiration')
def inspiration():
    links = list(fashion_links_col.find())
    return render_template('dashboard.html', section='inspiration', inspiration=links)

@app.route('/references')
def references():
    return render_template('dashboard.html', section='references')

@app.route('/hair-color')
def hair_color():
    return render_template('dashboard.html', section='hair')

@app.route('/saved-looks')
def saved_looks():
    outfits = list(saved_looks_col.find())
    return render_template('dashboard.html', section='saved', outfits=outfits)

@app.route('/settings')
def settings():
    return render_template('dashboard.html', section='settings')

# API Mock para guardar links
@app.route('/api/add-link', methods=['POST'])
def add_link():
    url = request.form.get('url')
    name = url.split('//')[-1].split('.')[0].capitalize()
    new_link = {
        "name": name,
        "url": url,
        "img": f"https://logo.clearbit.com/{url.split('//')[-1]}",
        "category": "Usuario",
        "favorite": False
    }
    fashion_links_col.insert_one(new_link)
    return redirect(url_for('inspiration'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
