from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from sqlalchemy import func
from config import Config
from database import db, init_db, User, Category, Product, PackagingStock, ProductPackagingMapping, Order, OrderItem, StockTransaction

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_sqlalchemy_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for frontend requests
CORS(app)

# Create upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize DB and seed
init_db(app)

# Serving uploaded product images
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ================= AUTH ENDPOINTS =================

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
        
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
        
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    })


# ================= CATEGORY ENDPOINTS =================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([cat.to_dict() for cat in categories])

@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.json or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category name already exists'}), 400
    new_cat = Category(name=name)
    db.session.add(new_cat)
    db.session.commit()
    return jsonify(new_cat.to_dict()), 201

@app.route('/api/categories/<int:id>', methods=['PUT'])
def update_category(id):
    cat = Category.query.get_or_404(id)
    data = request.json or {}
    name = data.get('name')
    if name:
        existing = Category.query.filter_by(name=name).first()
        if existing and existing.id != id:
            return jsonify({'error': 'Category name already exists'}), 400
        cat.name = name
        db.session.commit()
    return jsonify(cat.to_dict())

@app.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    cat = Category.query.get_or_404(id)
    if cat.name == 'Add-ons':
        return jsonify({'error': 'Cannot delete system default Add-ons category'}), 400
    # Update products in this category to be uncategorized
    Product.query.filter_by(category_id=id).update({Product.category_id: None})
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})



# ================= PRODUCT ENDPOINTS (WITH CRUD) =================

@app.route('/api/products', methods=['GET'])
def get_products():
    search = request.args.get('search', '')
    category_id = request.args.get('category_id')
    
    query = Product.query
    if search:
        query = query.filter(Product.name.like(f"%{search}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
        
    products = query.order_by(Product.name).all()
    return jsonify([prod.to_dict() for prod in products])

@app.route('/api/products', methods=['POST'])
def create_product():
    # Admin check would go here in production
    data = request.form.to_dict()
    
    # Handle optional image file
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename:
            filename = f"{int(datetime.now().timestamp())}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = f"/static/uploads/{filename}"

    # Extract details
    name = data.get('name')
    price = data.get('price')
    category_id = data.get('category_id')
    
    if not name or not price:
        return jsonify({'error': 'Product name and price are required'}), 400
        
    try:
        price = float(price)
    except ValueError:
        return jsonify({'error': 'Invalid price format'}), 400
        
    # Check uniqueness
    if Product.query.filter_by(name=name).first():
        return jsonify({'error': 'Product name already exists'}), 400
        
    new_prod = Product(
        name=name,
        price=price,
        category_id=category_id if category_id else None,
        image_url=image_url
    )
    
    db.session.add(new_prod)
    db.session.commit()
    
    # Map automatically based on category
    # (Just like we did during seeding, we can map dynamically)
    with app.app_context():
        # Retrieve freshly saved product with category relation
        saved_prod = Product.query.filter_by(name=name).first()
        if saved_prod and saved_prod.category:
            cat_name = saved_prod.category.name
            packaging_map = {item.name: item for item in PackagingStock.query.all()}
            
            # Helper function to map
            def add_mapping(order_type, pack_name, qty):
                if pack_name in packaging_map:
                    db.session.add(ProductPackagingMapping(
                        product_id=saved_prod.id,
                        order_type=order_type,
                        packaging_id=packaging_map[pack_name].id,
                        quantity=qty
                    ))
            
            if cat_name in ['Waffles', 'Waffwich']:
                add_mapping('Dine-In', 'Cone', 1)
                add_mapping('Parcel', 'Cone', 1)
                add_mapping('Parcel', 'Parcel Tray', 1)
            elif cat_name in ['Bisky Waffles', 'Chocolisious', 'Fruitfull Crunches'] or 'Ice Cream' in name:
                add_mapping('Dine-In', 'Pancake Tray', 1)
                add_mapping('Parcel', 'Parcel Tray', 1)
            elif cat_name in ['Churros', 'Maggi']:
                add_mapping('Dine-In', 'Parcel Tray', 1)
                add_mapping('Parcel', 'Parcel Tray', 1)
            elif cat_name == 'Fries':
                add_mapping('Dine-In', 'Pancake Tray', 1)
                add_mapping('Parcel', 'Parcel Tray', 1)
            elif cat_name in ['Milkshakes', 'Coffee Delights', 'Hot Chocoholic', 'Fizzy Pops']:
                add_mapping('Dine-In', '350ml Cup', 1)
                add_mapping('Parcel', '350ml Cup', 1)
            elif cat_name == 'Choco Bites':
                add_mapping('Dine-In', '250ml Cup', 1)
                add_mapping('Parcel', '250ml Cup', 1)
            elif cat_name in ['Sandwich', 'Long Bun Sandwich', 'Bombolinis']:
                add_mapping('Dine-In', 'Pancake Tray', 1)
                add_mapping('Parcel', 'Parcel Tray', 1)
            db.session.commit()
            
    return jsonify(new_prod.to_dict()), 210

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    prod = Product.query.get_or_404(id)
    data = request.form.to_dict()
    
    # Handle optional image file
    if 'image' in request.files:
        file = request.files['image']
        if file.filename:
            filename = f"{int(datetime.now().timestamp())}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Delete old image if it exists and was custom uploaded
            if prod.image_url and prod.image_url.startswith('/static/uploads/'):
                old_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), prod.image_url.lstrip('/'))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception:
                        pass
            prod.image_url = f"/static/uploads/{filename}"
            
    name = data.get('name')
    price = data.get('price')
    category_id = data.get('category_id')
    
    if name:
        # Check uniqueness if name changed
        existing = Product.query.filter_by(name=name).first()
        if existing and existing.id != id:
            return jsonify({'error': 'Product name already exists'}), 400
        prod.name = name
    if price:
        try:
            prod.price = float(price)
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400
    if category_id is not None:
        prod.category_id = int(category_id) if category_id else None
        
    db.session.commit()
    return jsonify(prod.to_dict())

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    prod = Product.query.get_or_404(id)
    # Delete uploaded file
    if prod.image_url and prod.image_url.startswith('/static/uploads/'):
        old_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), prod.image_url.lstrip('/'))
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass
    db.session.delete(prod)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})


# ================= PACKAGING STOCK ENDPOINTS =================

@app.route('/api/packaging', methods=['GET'])
def get_packaging():
    stock = PackagingStock.query.all()
    # Check if stock is below min levels for warning flag
    result = []
    for s in stock:
        d = s.to_dict()
        d['is_low'] = s.current_stock < s.min_stock
        result.append(d)
    return jsonify(result)

@app.route('/api/packaging/<int:id>', methods=['PUT'])
def update_packaging(id):
    item = PackagingStock.query.get_or_404(id)
    data = request.json or {}
    
    action = data.get('action')  # 'ADD' or 'UPDATE'
    qty = data.get('quantity')
    min_stock = data.get('min_stock')
    
    if min_stock is not None:
        try:
            item.min_stock = int(min_stock)
        except ValueError:
            return jsonify({'error': 'Min stock level must be an integer'}), 400
            
    if qty is not None:
        try:
            qty_val = int(qty)
        except ValueError:
            return jsonify({'error': 'Quantity must be an integer'}), 400
            
        if action == 'ADD':
            item.current_stock += qty_val
            txn = StockTransaction(
                packaging_id=item.id,
                transaction_type='ADD',
                quantity=qty_val,
                reference='Manual Stock Addition'
            )
            db.session.add(txn)
        elif action == 'UPDATE':
            diff = qty_val - item.current_stock
            item.current_stock = qty_val
            txn = StockTransaction(
                packaging_id=item.id,
                transaction_type='UPDATE',
                quantity=qty_val,
                reference=f'Manual Level Correction ({"+" if diff>=0 else ""}{diff} adjustment)'
            )
            db.session.add(txn)
            
    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/api/packaging/transactions', methods=['GET'])
def get_packaging_transactions():
    transactions = StockTransaction.query.order_by(StockTransaction.created_at.desc()).limit(100).all()
    return jsonify([t.to_dict() for t in transactions])


# ================= ORDERS & CHECKOUT ENDPOINTS =================

@app.route('/api/orders/check-stock', methods=['POST'])
def check_packaging_stock():
    """Dry-runs packaging stock check to see if order is possible."""
    data = request.json or {}
    order_type = data.get('order_type', 'Dine-In')
    items = data.get('items', [])
    
    if not items:
        return jsonify({'success': True})
        
    needed_packaging = {}
    for item in items:
        prod_id = item.get('product_id')
        qty = item.get('quantity', 1)
        item_order_type = item.get('order_type', order_type)
        
        # Query mappings for this product + item_order_type
        mappings = ProductPackagingMapping.query.filter_by(
            product_id=prod_id,
            order_type=item_order_type
        ).all()
        
        for m in mappings:
            pack_id = m.packaging_id
            needed_packaging[pack_id] = needed_packaging.get(pack_id, 0) + (m.quantity * qty)
            
    # Compare with current stock levels
    insufficient = []
    for pack_id, required_qty in needed_packaging.items():
        pack_item = PackagingStock.query.get(pack_id)
        if pack_item and pack_item.current_stock < required_qty:
            insufficient.append({
                'id': pack_item.id,
                'name': pack_item.name,
                'available': pack_item.current_stock,
                'required': required_qty
            })
            
    if insufficient:
        return jsonify({
            'success': False,
            'error': 'Insufficient packaging stock',
            'insufficient': insufficient
        }), 400
        
    return jsonify({'success': True})

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json or {}
    order_type = data.get('order_type', 'Dine-In')
    items = data.get('items', [])
    cashier_id = data.get('cashier_id')
    
    if not items:
        return jsonify({'error': 'No items in the order'}), 400
        
    # Start checking packaging stock (dry-run again for safety inside transaction)
    needed_packaging = {}
    cart_products = {}
    
    for item in items:
        prod_id = item.get('product_id')
        qty = item.get('quantity', 1)
        item_order_type = item.get('order_type', order_type)
        
        # Load product details
        prod = Product.query.get(prod_id)
        if not prod:
            return jsonify({'error': f'Product ID {prod_id} not found'}), 404
            
        cart_products[prod_id] = prod
        
        # Do not compute packaging rules for Add-ons category items themselves
        if prod.category and prod.category.name == 'Add-ons':
            continue
            
        # Get packaging maps
        mappings = ProductPackagingMapping.query.filter_by(
            product_id=prod_id,
            order_type=item_order_type
        ).all()
        
        for m in mappings:
            pack_id = m.packaging_id
            needed_packaging[pack_id] = needed_packaging.get(pack_id, 0) + (m.quantity * qty)
            
    # Check packaging quantities
    insufficient = []
    for pack_id, required_qty in needed_packaging.items():
        pack_item = PackagingStock.query.get(pack_id)
        if pack_item and pack_item.current_stock < required_qty:
            insufficient.append({
                'id': pack_item.id,
                'name': pack_item.name,
                'available': pack_item.current_stock,
                'required': required_qty
            })
            
    if insufficient:
        return jsonify({
            'error': 'Checkout blocked: Required packaging stock unavailable.',
            'insufficient': insufficient
        }), 400

    try:
        # 1. Generate unique sequential bill number: WFL-YYYYMMDD-XXXX
        today_str = datetime.now().strftime('%Y%m%d')
        # Count orders placed today
        start_of_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        orders_today_count = Order.query.filter(Order.created_at >= start_of_today).count()
        bill_number = f"WFL-{today_str}-{(orders_today_count + 1):04d}"

        # Determine overall order type based on item-level order types
        item_types = set(item.get('order_type', order_type) for item in items if cart_products[item.get('product_id')].category and cart_products[item.get('product_id')].category.name != 'Add-ons')
        if len(item_types) == 1:
            header_order_type = list(item_types)[0]
        elif len(item_types) > 1:
            header_order_type = 'Mixed'
        else:
            header_order_type = order_type

        # 2. Compute bill amounts
        subtotal = 0.0
        parcel_charge_total = 0.0
        
        order_items_to_save = []
        
        for item in items:
            prod_id = item.get('product_id')
            qty = item.get('quantity', 1)
            item_order_type = item.get('order_type', order_type)
            prod = cart_products[prod_id]
            
            # Base price of item
            base_price = prod.price
            
            # Parcel pricing rule: menu price + ₹10. Show parcel charge separately.
            item_parcel_charge = 0.0
            if item_order_type == 'Parcel':
                # Only charge parcel fees on non-add-ons
                if prod.category and prod.category.name != 'Add-ons':
                    item_parcel_charge = 10.0
                    
            item_subtotal = (base_price * qty)
            subtotal += item_subtotal
            parcel_charge_total += (item_parcel_charge * qty)
            
            order_item = OrderItem(
                product_id=prod.id,
                product_name=prod.name,
                price=base_price,
                quantity=qty,
                parcel_charge_item=item_parcel_charge,
                subtotal=item_subtotal + (item_parcel_charge * qty)
            )
            order_items_to_save.append(order_item)
            
        grand_total = subtotal + parcel_charge_total
        
        # 3. Save Order Header
        new_order = Order(
            bill_number=bill_number,
            order_type=header_order_type,
            subtotal=subtotal,
            parcel_charge=parcel_charge_total,
            grand_total=grand_total,
            cashier_id=cashier_id
        )
        db.session.add(new_order)
        db.session.flush() # Populate new_order.id
        
        # 4. Save Order Items
        for order_item in order_items_to_save:
            order_item.order_id = new_order.id
            db.session.add(order_item)
            
        # 5. Deduct packaging stock and log transaction
        for pack_id, required_qty in needed_packaging.items():
            pack_item = PackagingStock.query.get(pack_id)
            pack_item.current_stock -= required_qty
            
            txn = StockTransaction(
                packaging_id=pack_id,
                transaction_type='DEDUCT',
                quantity=required_qty,
                reference=f"Order {bill_number}"
            )
            db.session.add(txn)
            
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Order placed successfully',
            'order': new_order.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to place order: {str(e)}'}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.order_by(Order.created_at.desc()).limit(100).all()
    return jsonify([ord.to_dict() for ord in orders])


# ================= DASHBOARD ANALYTICS ENDPOINTS =================

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    now = datetime.now()
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_today - timedelta(days=6)
    start_of_month = start_of_today - timedelta(days=29)
    
    # 1. Sales stats
    today_sales = db.session.query(func.sum(Order.grand_total)).filter(Order.created_at >= start_of_today).scalar() or 0.0
    weekly_sales = db.session.query(func.sum(Order.grand_total)).filter(Order.created_at >= start_of_week).scalar() or 0.0
    monthly_sales = db.session.query(func.sum(Order.grand_total)).filter(Order.created_at >= start_of_month).scalar() or 0.0
    
    # 2. Order counts
    today_orders = Order.query.filter(Order.created_at >= start_of_today).count()
    weekly_orders = Order.query.filter(Order.created_at >= start_of_week).count()
    monthly_orders = Order.query.filter(Order.created_at >= start_of_month).count()
    
    # 3. Low stock alerts
    low_stock = PackagingStock.query.filter(PackagingStock.current_stock < PackagingStock.min_stock).all()
    low_stock_alerts = [item.to_dict() for item in low_stock]
    
    # 4. Top Selling Products (all time or monthly)
    top_selling_raw = db.session.query(
        OrderItem.product_name,
        func.sum(OrderItem.quantity).label('total_qty')
    ).group_by(OrderItem.product_name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
    
    top_selling = [{'name': name, 'quantity': int(qty)} for name, qty in top_selling_raw]
    
    # 5. Revenue chart data (last 7 days)
    revenue_chart = []
    for i in range(7):
        day = start_of_today - timedelta(days=6-i)
        day_end = day + timedelta(days=1)
        day_revenue = db.session.query(func.sum(Order.grand_total)).filter(
            Order.created_at >= day,
            Order.created_at < day_end
        ).scalar() or 0.0
        revenue_chart.append({
            'date': day.strftime('%Y-%m-%d'),
            'label': day.strftime('%a'),
            'revenue': float(day_revenue)
        })
        
    # 6. Packaging Stock Consumption Report
    consumption_raw = db.session.query(
        PackagingStock.name,
        func.sum(StockTransaction.quantity).label('total_qty')
    ).join(StockTransaction).filter(
        StockTransaction.transaction_type == 'DEDUCT',
        StockTransaction.created_at >= start_of_month
    ).group_by(PackagingStock.name).all()
    
    consumption_report = [{'name': name, 'quantity': int(qty)} for name, qty in consumption_raw]
    
    return jsonify({
        'today_sales': float(today_sales),
        'weekly_sales': float(weekly_sales),
        'monthly_sales': float(monthly_sales),
        'today_orders': today_orders,
        'weekly_orders': weekly_orders,
        'monthly_orders': monthly_orders,
        'low_stock_alerts': low_stock_alerts,
        'top_selling': top_selling,
        'revenue_chart': revenue_chart,
        'consumption_report': consumption_report
    })


# Serve static build of React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
    if path != "" and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, 'index.html')


if __name__ == '__main__':
    # Serve locally on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
