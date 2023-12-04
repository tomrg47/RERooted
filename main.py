import json,os
from flask import Flask, jsonify, render_template, request,redirect,url_for


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


def create_user(username, password):
    users_data = load_users()
    new_user = {
        "username": username,
        "password": password,
        "account_level": "basic"  # You can set a default account level here
    }
    users_data['users'].append(new_user)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        create_user(new_username, new_password)

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
@app.route('/list_item', methods=['GET','POST'])
def list_item():
  if request.method == 'POST':
   # Access form data using request.form and request.files
    product_name = request.form['productName']
    price = float(request.form['price'])
    size = request.form['size']
    brand = request.form['brand']
    colour = request.form['colour']
    location = request.form['location']
    description = request.form['description']

    # Assuming 'photo' is the name attribute of the file input
    photo_file = request.files['photo']

    # Generate a unique ID for the new product
    new_product_id = len(products) + 1

    # Save the uploaded photo with a unique filename
    photo_filename = f"product_{new_product_id}.jpg"  # You can use a more sophisticated approach for filenames
    photo_path = os.path.join('static', 'images', photo_filename)
    photo_file.save(photo_path)
    
    # Get the current date and time
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add the new product to the products list
    new_product = {
        'id': new_product_id,
        'name': product_name,
        'dateListed': upload_date,
        'image': f'images/uploads/{photo_filename}',
        'description': description,
        'price': price,
        'productState': "Available",
        'size': size,
        'brand': brand,
        'colour': colour,
        'location': location
    }

    products.append(new_product)

    # Save the updated products list to the JSON file
    save_product_data(products)
  
    return render_template('for_sale.html', product = new_product)
  else:
    return render_template('for_sale.html')
  
if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=8080, debug=True)



#datetime.now().isoformat()