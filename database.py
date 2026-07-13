from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='cashier') # 'cashier', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    mappings = db.relationship('ProductPackagingMapping', backref='product', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else 'Uncategorized',
            'name': self.name,
            'price': self.price,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat()
        }

class PackagingStock(db.Model):
    __tablename__ = 'packaging_stock'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    current_stock = db.Column(db.Integer, nullable=False, default=0)
    min_stock = db.Column(db.Integer, nullable=False, default=10)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    transactions = db.relationship('StockTransaction', backref='packaging', lazy=True, cascade='all, delete-orphan')
    mappings = db.relationship('ProductPackagingMapping', backref='packaging', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'current_stock': self.current_stock,
            'min_stock': self.min_stock,
            'last_updated': self.last_updated.isoformat()
        }

class ProductPackagingMapping(db.Model):
    __tablename__ = 'product_packaging_mapping'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    order_type = db.Column(db.String(10), nullable=False)  # 'Dine-In' or 'Parcel'
    packaging_id = db.Column(db.Integer, db.ForeignKey('packaging_stock.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    __table_args__ = (
        db.UniqueConstraint('product_id', 'order_type', 'packaging_id', name='uq_prod_type_pack'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else 'Unknown',
            'order_type': self.order_type,
            'packaging_id': self.packaging_id,
            'packaging_name': self.packaging.name if self.packaging else 'Unknown',
            'quantity': self.quantity
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    order_type = db.Column(db.String(10), nullable=False)  # 'Dine-In', 'Parcel'
    subtotal = db.Column(db.Float, nullable=False)
    parcel_charge = db.Column(db.Float, nullable=False, default=0.00)
    grand_total = db.Column(db.Float, nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    cashier = db.relationship('User', backref='orders', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'bill_number': self.bill_number,
            'order_type': self.order_type,
            'subtotal': self.subtotal,
            'parcel_charge': self.parcel_charge,
            'grand_total': self.grand_total,
            'cashier_id': self.cashier_id,
            'cashier_name': self.cashier.username if self.cashier else 'System',
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    parcel_charge_item = db.Column(db.Float, nullable=False, default=0.00)
    subtotal = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'price': self.price,
            'quantity': self.quantity,
            'parcel_charge_item': self.parcel_charge_item,
            'subtotal': self.subtotal
        }

class StockTransaction(db.Model):
    __tablename__ = 'stock_transactions'
    id = db.Column(db.Integer, primary_key=True)
    packaging_id = db.Column(db.Integer, db.ForeignKey('packaging_stock.id', ondelete='CASCADE'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'ADD', 'DEDUCT', 'UPDATE'
    quantity = db.Column(db.Integer, nullable=False)
    reference = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'packaging_id': self.packaging_id,
            'packaging_name': self.packaging.name if self.packaging else 'Unknown',
            'transaction_type': self.transaction_type,
            'quantity': self.quantity,
            'reference': self.reference,
            'created_at': self.created_at.isoformat()
        }


def init_db(app):
    if not Config.USE_SQLITE:
        # Create MySQL database if it doesn't exist
        try:
            connection = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=int(Config.DB_PORT)
            )
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                connection.commit()
                print(f"Verified or created MySQL database '{Config.DB_NAME}'")
            finally:
                connection.close()
        except Exception as e:
            print(f"Error creating MySQL database: {e}")
            print("Switching configurations to SQLite fallback due to connection failure...")
            Config.USE_SQLITE = True

    # Re-evaluate and set correct SQLAlchemy URI
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_sqlalchemy_database_uri()
    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_all_data()


def seed_all_data():
    from seed_data import CATEGORIES, PRODUCTS, PACKAGING_ITEMS, CATEGORY_IMAGES
    
    # 1. Seed Default Users
    # Remove old default users if they exist
    old_admin = User.query.filter_by(username='admin').first()
    if old_admin:
        db.session.delete(old_admin)
        print("Removed legacy 'admin' user")
        
    old_cashier = User.query.filter_by(username='cashier').first()
    if old_cashier:
        db.session.delete(old_cashier)
        print("Removed legacy 'cashier' user")

    # Seed SugarWheels (admin)
    admin_user = User.query.filter_by(username='SugarWheels').first()
    if admin_user is None:
        admin_user = User(username='SugarWheels', role='admin')
        admin_user.set_password('sugar@20')
        db.session.add(admin_user)
        print("Seeded 'SugarWheels' admin user")
    else:
        admin_user.set_password('sugar@20')
        admin_user.role = 'admin'

    # Seed Shyamsugar (cashier)
    cashier_user = User.query.filter_by(username='Shyamsugar').first()
    if cashier_user is None:
        cashier_user = User(username='Shyamsugar', role='cashier')
        cashier_user.set_password('Shyam@250')
        db.session.add(cashier_user)
        print("Seeded 'Shyamsugar' cashier user")
    else:
        cashier_user.set_password('Shyam@250')
        cashier_user.role = 'cashier'
        
    db.session.commit()
        
    # 2. Seed Categories
    category_map = {}
    for cat_name in CATEGORIES:
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name)
            db.session.add(cat)
            db.session.flush()
        category_map[cat_name] = cat
        
    # 3. Seed Packaging Stock
    packaging_map = {}
    for pack in PACKAGING_ITEMS:
        item = PackagingStock.query.filter_by(name=pack['name']).first()
        if not item:
            item = PackagingStock(
                name=pack['name'],
                current_stock=pack['current_stock'],
                min_stock=pack['min_stock']
            )
            db.session.add(item)
            db.session.flush()
            
            # Record initial stock transaction
            txn = StockTransaction(
                packaging_id=item.id,
                transaction_type='ADD',
                quantity=pack['current_stock'],
                reference='Initial Seed Stock'
            )
            db.session.add(txn)
        packaging_map[pack['name']] = item

    # 4. Seed Products
    product_map = {}
    for prod_info in PRODUCTS:
        prod = Product.query.filter_by(name=prod_info['name']).first()
        if not prod:
            cat = category_map.get(prod_info['category'])
            img_url = CATEGORY_IMAGES.get(prod_info['category'], None)
            prod = Product(
                name=prod_info['name'],
                price=prod_info['price'],
                category_id=cat.id if cat else None,
                image_url=img_url
            )
            db.session.add(prod)
            db.session.flush()
        product_map[prod.name] = prod

    # 5. Seed Product Packaging Mappings (if mappings empty)
    if ProductPackagingMapping.query.first() is None:
        print("Seeding product-to-packaging mappings...")
        for prod_name, prod in product_map.items():
            cat_name = prod.category.name if prod.category else None
            
            # Waffles & Waffwich
            # Dine-In: Cone (1)
            # Parcel: Cone (1) + Parcel Tray (1)
            if cat_name in ['Waffles', 'Waffwich']:
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['Cone'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['Cone'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
            
            # Bisky Waffles, Chocolisious (Brownie, Lava Cake), Fruitfull Crunches, or name includes Ice Cream
            # Dine-In: Pancake Tray (1)
            # Parcel: Parcel Tray (1)
            elif cat_name in ['Bisky Waffles', 'Chocolisious', 'Fruitfull Crunches'] or 'Ice Cream' in prod_name:
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['Pancake Tray'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
                
            # Churros: Dine-In -> Parcel Tray, Parcel -> Parcel Tray
            elif cat_name == 'Churros':
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
                
            # Fries: Dine-In -> Pancake Tray, Parcel -> Parcel Tray
            elif cat_name == 'Fries':
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['Pancake Tray'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
                
            # Maggi: Dine-In -> Parcel Tray, Parcel -> Parcel Tray
            elif cat_name == 'Maggi':
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
                
            # Milkshakes, Coffee Delights, Hot Chocoholic, Fizzy Pops:
            # Dine-In -> 350ml Cup, Parcel -> 350ml Cup
            elif cat_name in ['Milkshakes', 'Coffee Delights', 'Hot Chocoholic', 'Fizzy Pops']:
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['350ml Cup'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['350ml Cup'].id, quantity=1))
                
            # Choco Bites: Dine-In -> 250ml Cup, Parcel -> 250ml Cup
            elif cat_name == 'Choco Bites':
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['250ml Cup'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['250ml Cup'].id, quantity=1))
            
            # Sandwiches, Long Bun Sandwiches, Bombolinis
            elif cat_name in ['Sandwich', 'Long Bun Sandwich', 'Bombolinis']:
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Dine-In', packaging_id=packaging_map['Pancake Tray'].id, quantity=1))
                db.session.add(ProductPackagingMapping(product_id=prod.id, order_type='Parcel', packaging_id=packaging_map['Parcel Tray'].id, quantity=1))
                
    db.session.commit()
    print("Database seeding completed successfully.")
