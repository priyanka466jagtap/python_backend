from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
if __package__:
    from .models import Product
    from .database import session, engine
    from . import database_models
else:
    from models import Product
    from database import session, engine
    import database_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://python-frontend.vercel.app"],
    allow_methods=["*"]
)

# Create database tables
database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Welcome to Telusko Track"


# Initial products
products = [
    Product(
        id=1,
        name="phone",
        description="budget phone",
        price=99,
        quantity=10
    ),
    Product(
        id=2,
        name="laptop",
        description="Gaming Laptop",
        price=991,
        quantity=100
    ),
    Product(
        id=3,
        name="pen",
        description="pen description",
        price=200,
        quantity=100
    ),
    Product(
        id=4,
        name="table",
        description="table description",
        price=91,
        quantity=500
    ),
]


# Database dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# Insert initial products into database
def init_db():
    db = session()

    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db_product = database_models.Product(
                **product.model_dump()
            )

            db.add(db_product)

        db.commit()

    db.close()


init_db()


# --------------------------------
# GET ALL PRODUCTS
# --------------------------------

@app.get("/products")
def get_all_product(db=Depends(get_db)):

    db_products = db.query(database_models.Product).all()

    return db_products


# --------------------------------
# GET PRODUCT BY ID
# --------------------------------

@app.get("/product/{id}")
def get_product_by_id(id: int, db=Depends(get_db)):

    product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if product:
        return product

    return "Product not found"


# --------------------------------
# ADD PRODUCT
# --------------------------------

@app.post("/products")
def add_product(product: Product, db=Depends(get_db)):

    # Check if product ID already exists
    existing_product = db.query(database_models.Product).filter(
        database_models.Product.id == product.id
    ).first()

    if existing_product:
        return "Product with this ID already exists"

    db_product = database_models.Product(
        **product.model_dump()
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


# --------------------------------
# UPDATE PRODUCT
# --------------------------------

@app.put("/products/{id}")
def update_product(
    id: int,
    product: Product,
    db=Depends(get_db)
):

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        return "Product not found"

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)

    return db_product


# --------------------------------
# DELETE PRODUCT
# --------------------------------

@app.delete("/products/{id}")
def delete_product(id: int, db=Depends(get_db)):

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        return "Product not found"

    db.delete(db_product)
    db.commit()

    return "Product deleted successfully"
