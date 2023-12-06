import json,os
#from datetime import datetime
from flask import Flask, jsonify, render_template, request, session


app = Flask(__name__)
app.secret_key = 'group_15'

# Load user data from the JSON file
def load_users():
    script_dir = os.path.dirname(__file__)
    relative_path = 'data/users.json'

    # Form the absolute path using the script directory and relative path
    abs_file_path = os.path.join(script_dir, relative_path)
    with open(abs_file_path, 'r') as file:
        users_data = json.load(file)
        return users_data['users']

users = load_users()

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

def save_users_data(users):
    script_dir = os.path.dirname(__file__)
    relative_path = 'data/users.json'
    abs_file_path = os.path.join(script_dir, relative_path)
    with open(abs_file_path, 'w') as file:
        json.dump({'users': users}, file, indent=2)

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
            session['is_authenticated'] = True
            # Optionally, you can store additional user-related data in the session
            session['username'] = username
            session['account_level'] = account_level
            return render_template('home.html', is_authenticated=True)
        else:
            return "Invalid credentials. Please try again."
    return render_template('log_in.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Access form data using request.form and request.files
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        # Generate a unique ID for the user
        new_user_id = "basic_" + str(len(users) + 1)

        # Add the new user to the users list
        new_user = {
            "username": new_username,
            "password": new_password,
            "account_level": "basic",
            "user_id": new_user_id
        }

        users.append(new_user)

        save_users_data(users)

        return f"Account created for {new_username}!"

    # If it's a GET request or the form was not submitted, render the signup form
    return render_template('log_in.html')

@app.route('/view_profile')
def view_profile():
    # Assume you have user data stored in the session after login
    # You may need to adjust this based on your actual user management logic
    user_data = session.get('user_data', {})

    return render_template('profile.html', user=user_data)


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
        photo_filename = f"product_{new_product_id}.jpg" 
        photo_path = os.path.join('static', 'images', photo_filename)
        photo_file.save(photo_path)

        #upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the new product to the products list
        new_product = {
            'id': new_product_id,
            'userId': 'upload_date',
            'name': product_name,
            'dateListed': 'placeholder',
            'image': f'static/images/{photo_filename}',
            'description': description,
            'price': price,
            'productState': False,
            'brand': brand,
            'size': size,
            'colour': colour,
            'location': location
        }

        products.append(new_product)

        # Save the updated products list to the JSON file
        save_product_data(products)

        return render_template('list_item.html', product = new_product)
    else:
        return render_template('list_item.html')

    
  
if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=8080, debug=True)



#datetime.now().isoformat()