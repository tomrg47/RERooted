import json,os
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

# Load user data from the JSON file
def load_users():
    script_dir = os.path.dirname(__file__)
    relative_path = 'data/users.json'

    # Form the absolute path using the script directory and relative path
    abs_file_path = os.path.join(script_dir, relative_path)
    with open(abs_file_path, 'r') as file:
        users_data = json.load(file)
        return users_data['users']

# Load product data from the JSON file
def load_product_data():
    script_dir = os.path.dirname(__file__)
    relative_path = 'data/products.json'

    # Form the absolute path using the script directory and relative path
    abs_file_path = os.path.join(script_dir, relative_path)

    with open(abs_file_path, 'r') as file:
        products = json.load(file)
        return products['products']

products = load_product_data()

def save_product_data(products):
    script_dir = os.path.dirname(__file__)
    relative_path = 'data/products.json'
    abs_file_path = os.path.join(script_dir, relative_path)
    with open(abs_file_path, 'w') as file:
        json.dump({'products': products}, file, indent=2)

# Verify login credentials
def verify_login(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True, user['account_level']
    return False, None

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_valid, account_level = verify_login(username, password)
        if is_valid:
            # Perform actions based on account level (redirect to different pages, etc.)
            return render_template('home.html')
        else:
            return "Invalid credentials. Please try again."
    return render_template('log_in.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        request.form['new_password']

        # Here, you'd typically add the new user to your database or user repository
        # For this example, let's assume you have a function called `create_user`
        # This is where you'd handle the creation of the new user account
        # create_user(new_username, new_password)

        return f"Account created for {new_username}!"

    # If it's a GET request or the form was not submitted, render the signup form
    return render_template('log_in.html')



@app.route('/get_products')
def get_products():
    return jsonify(products)

@app.route('/item/<int:item_id>')
def item(item_id):
  
  item = next((product for product in products if product["id"] == item_id), None)

  if item:
      # Format the price as a string
      item["price_formatted"] = "£{:.2f}".format(item["price"])
      return render_template('item.html', item=item)
  else:
      return render_template('error.html', message="Product not found")

# Handle form submission to add a new product
@app.route('/sell', methods=['POST'])
def sell():
    # Access form data using request.form and request.files
    product_name = request.form['productName']
    price = float(request.form['price'])
    size = request.form['size']
    brand = request.form['brand']
    color = request.form['color']
    location = request.form['location']
    description = request.form['description']

    # Assuming 'photo' is the name attribute of the file input
    photo_file = request.files['photo']

    # Generate a unique ID for the new product
    new_product_id = len(products) + 1

    # Save the uploaded photo with a unique filename
    photo_filename = f"product_{new_product_id}.jpg"  # You can use a more sophisticated approach for filenames
    photo_path = os.path.join('static', 'images', 'uploads', photo_filename)
    photo_file.save(photo_path)

    # Add the new product to the products list
    new_product = {
        'id': new_product_id,
        'name': product_name,
        'price': price,
        'size': size,
        'brand': brand,
        'color': color,
        'location': location,
        'description': description,
        'image': f'images/uploads/{photo_filename}'  # Update with the correct path to the uploaded image
    }

    products.append(new_product)

    # Save the updated products list to the JSON file
    save_product_data(products)

    return redirect(url_for('get_products'))
  
if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=8080, debug=True)



#datetime.now().isoformat()