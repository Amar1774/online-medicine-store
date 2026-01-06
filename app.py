from flask import Flask, render_template, request, redirect, url_for, jsonify,session,flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sai kiran'

users = [] # Mock database
products = [
    {"id": 1, "name": "Paracetamol 500mg", "price": 20, "description": "Relieves fever and mild pain.", "image":"https://media.istockphoto.com/id/1222003499/photo/generic-paracetamol-pills.jpg?s=612x612&w=0&k=20&c=oGTaD42V9qcko4cKEsp9q08TG5oBQzGbWvAjPmxF6o0="},
    {"id": 2, "name": "Ibuprofen 400mg", "price": 30, "description": "Reduces inflammation and pain.","image":"https://www.youngsurgicalsolutions.com/_next/image?url=https://shop.youngsurgicalsolutions.com/media/catalog/product/i/b/ibup-main_slhuj4yjmf5mc0u9.jpeg&w=3840&q=75"},
    {"id": 3, "name": "Cough Syrup", "price": 60, "description": "Relieves cough and throat irritation.","image":"https://hylands.com/cdn/shop/files/KCMDNOLF1-4Z2PK_H1_01_1445x.webp?v=1743714222"}
]

cart = []

@app.route('/')
def home():
    if 'username' in session:  # Check if user is logged in
        return render_template('index.html', products=products)  # Show products if logged in
    return redirect(url_for('login'))  # Redirect to login page if not logged in

@app.route('/products')
def product_list():
     return render_template('medicines.html', products=products)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    results = [p for p in products if query in p['name'].lower()]
    return render_template('index.html', products=results)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password are correct
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = username  # Store the username in session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to the main page
        else:
            flash('Invalid credentials. Please try again or register.', 'danger')
    
    return render_template('login.html')  # Show login form
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from session to log out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        if next((u for u in users if u['username'] == username), None):
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Add the new user to the users list
            users.append({"username": username, "password": password})
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))  # Redirect to login page after successful registration
    
    return render_template('register.html')  # Show register form


@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/addToCart', methods=['POST'])
def addToCart():
    product_id = request.json.get('product_id')
    try:
        product_id = int(product_id)  # convert to int here
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid product ID"}), 400

    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        cart.append(product)
        return jsonify({"message": "Added to cart"}), 200
    return jsonify({"message": "Product not found"}), 404
@app.route('/removeFromCart', methods=['POST'])
def removeFromCart():
    product_id = request.json.get('product_id')
    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid product ID"}), 400

    product = next((item for item in cart if item['id'] == product_id), None)
    if product:
        cart.remove(product)
        return jsonify({"message": "Removed from cart"}), 200
    return jsonify({"message": "Product not found in cart"}), 404



@app.route('/cart')
def view_cart():
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)


@app.route('/contact')
def contact():
    return "<h2>Contact us at support@healthplus.com /call us 7981097699</h2>"

if __name__ == '__main__':
    app.run(debug=True)
