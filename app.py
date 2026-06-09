import io
import os
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for, session, flash
from pymongo import MongoClient
from functools import wraps
from datetime import datetime
import uuid
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Fallback provided for safety, but will prioritize the environment variable
app.secret_key = os.getenv('SECRET_KEY', 'a_very_secret_fallback_key_123987')  

# ============================
# Database Configuration
# ============================
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)  
db = client['restaurant']  
tablebook_collection = db['tablebook']
contact_collection = db['contact']
orders_collection = db['orders']

# ============================
# Secure Admin Credentials
# ============================
# Fetching from environment variables with plain-text defaults for safe local testing
ADMIN_USERNAME = os.getenv('ADMIN_USER', 'nirvana')
PLAIN_PASSWORD = os.getenv('ADMIN_PASS', 'nirva1357')

# Securely hash the password string immediately upon setup
ADMIN_PASSWORD_HASH = generate_password_hash(PLAIN_PASSWORD)

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================
# Existing Routes for Main Pages
# ============================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

# Routes for Menu Items
@app.route('/food')
def food():
    return render_template('food.html')  

@app.route('/vegsoup')
def vegsoup():
    return render_template('vegsoup.html')  

@app.route('/chickensoup')
def chickensoup():
    return render_template('chickensoup.html') 

@app.route('/specialChickenBiryani')
def specialChickenBiryani():
    return render_template('specialChickenBiryani.html')  

@app.route('/dum')
def dum():
    return render_template('dum.html')  

@app.route('/eggbiryani')
def eggbiryani():
    return render_template('eggbiryani.html')  

@app.route('/muttonBiryanii')
def muttonBiryanii():
    return render_template('muttonBiryanii.html')  

@app.route('/prawns')
def prawns():
    return render_template('prawns.html')  

@app.route('/vegBiryani')
def vegBiryani():
    return render_template('vegBiryani.html')  

@app.route('/paneer')
def paneer():
    return render_template('paneer.html')  

@app.route('/mushroom')
def mushroom():
    return render_template('mushroom.html')  

@app.route('/ChocolateStrawberryCrumble')
def ChocolateStrawberryCrumble():
    return render_template('Chocolate Strawberry-Crumble.html')  

@app.route('/RedVelVetCake')
def RedVelVetCake():
    return render_template('RedVelVetCake.html')  

@app.route('/gulab')
def gulab():
    return render_template('gulab.html')  

@app.route('/orders')
def orders():
    return render_template('orders.html') 

@app.route('/dragonChicken')
def dragonChicken():
    return render_template('dragonChicken.html')  

@app.route('/PaneerTikka')
def PaneerTikka():
    return render_template('Paneer Tikka.html')  

@app.route('/veg')
def veg():
    return render_template('veg.html')  

@app.route('/qr')
def qr():
    return render_template('qr.html')

# ============================
# Existing Functional Routes
# ============================

@app.route('/reserve', methods=['POST'])
def reserve():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    booking_datetime = request.form['booking_datetime']
    number_of_people = request.form['number_of_people']
    email = request.form['email']
    phone = request.form['phone']
    food_orders = request.form.getlist('food_order')

    order_id = str(uuid.uuid4())  
    booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  

    reservation = {
        'order_id': order_id,  
        'booking_time': booking_time,  
        'first_name': first_name,
        'last_name': last_name,
        'booking_datetime': booking_datetime,
        'number_of_people': number_of_people,
        'email': email,
        'phone': phone,
        'food_orders': food_orders
    }

    tablebook_collection.insert_one(reservation)

    text_content = f"""
    Reservation Details:
    Order ID: {order_id}
    Booking Time: {booking_time}
    First Name: {first_name}
    Last Name: {last_name}
    Booking DateTime: {booking_datetime}
    Number of People: {number_of_people}
    Email: {email}
    Phone: {phone}
    Food Orders: {', '.join(food_orders)}
    """

    output = io.BytesIO(text_content.encode())
    output.seek(0)

    return send_file(output, mimetype='text/plain', as_attachment=True, download_name='reservation.txt')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/confirmation')
def confirmation():
    return render_template('paymentconfirm.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    data = {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    }
    contact_collection.insert_one(data)
    return redirect(url_for('contacts'))

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        order_data = request.json

        user_details = order_data.get('userDetails')
        order_items = order_data.get('orderItems')
        total_cost = order_data.get('totalCost')
        payment_method = order_data.get('paymentMethod')

        order_id = str(uuid.uuid4())  
        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  

        order_document = {
            'order_id': order_id,  
            'order_time': order_time,  
            'user_details': user_details,
            'order_items': order_items,
            'total_cost': total_cost,
            'payment_method': payment_method
        }

        orders_collection.insert_one(order_document)

        return jsonify({'success': True, 'order_id': order_id, 'order_time': order_time})

    return render_template('payment.html')

# ============================
# Admin Authentication Routes (SECURED)
# ============================

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Secured using constant-time hash verification check instead of plain-text equality
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            flash('Successfully logged in as admin.', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
    
    return render_template('admin_login.html', error=error)

@app.route('/dashboard')
@login_required
def dashboard():
    tablebook = list(tablebook_collection.find())
    contacts = list(contact_collection.find())
    orders = list(orders_collection.find())
    
    for booking in tablebook:
        booking['_id'] = str(booking['_id'])
        booking['booking_time'] = booking.get('booking_time', '')  
        booking['order_id'] = booking.get('order_id', '')  
    for contact in contacts:
        contact['_id'] = str(contact['_id'])
    for order in orders:
        order['_id'] = str(order['_id'])
        order['order_time'] = order.get('order_time', '')  
        order['order_id'] = order.get('order_id', '')  
        if 'user_details' in order and isinstance(order['user_details'], dict):
            order['user_details'] = {
                'name': order['user_details'].get('name', ''),
                'email': order['user_details'].get('email', '')
            }
    
    return render_template('dashboard.html', tablebook=tablebook, contacts=contacts, orders=orders)

@app.route('/admin_logout', methods=['POST'])
@login_required
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('', 'success')  
    return redirect(url_for('home'))

# ============================
# New Routes for Clearing Data
# ============================

@app.route('/clear_tablebook', methods=['POST'])
@login_required
def clear_tablebook():
    result = tablebook_collection.delete_many({})
    flash(f'Cleared {result.deleted_count} table booking records.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/clear_contacts', methods=['POST'])
@login_required
def clear_contacts():
    result = contact_collection.delete_many({})
    flash(f'Cleared {result.deleted_count} contact messages.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/clear_orders', methods=['POST'])
@login_required
def clear_orders():
    result = orders_collection.delete_many({})
    flash(f'Cleared {result.deleted_count} orders.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/clear_all', methods=['POST'])
@login_required
def clear_all():
    tablebook_result = tablebook_collection.delete_many({})
    contacts_result = contact_collection.delete_many({})
    orders_result = orders_collection.delete_many({})
    flash(f'Cleared {tablebook_result.deleted_count} table bookings, {contacts_result.deleted_count} contact messages, and {orders_result.deleted_count} orders.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)