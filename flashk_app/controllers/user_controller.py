from flashk_app import app
from flashk_app.models.order_model import Order
from flask import render_template,redirect,request,session,flash
from flashk_app.models.user_model import User
from flashk_app.models.menu_model import Menu
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#WELCOME ROUTE - RENDERS MENUS

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/welcome')
    return render_template('index.html')

@app.route('/welcome')
def showuser():
    if not 'user_id' in session:
        return redirect('/')
    
    data= { 'id' : session['user_id'] }
    menu = {'id': '1'}
    user_by_id = User.get_by_id(data)    
    one_menu = Menu.get_by_id(menu)
   
  
    return render_template('welcome.html', user_by_id = user_by_id, one_menu = one_menu)

@app.route('/create', methods=['POST'])
def create():

    if not User.validate_user(request.form):
    # redirect to the route where the user form is rendered.
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        "password" : pw_hash
    }

    # else no errors:
    session['user_id'] = User.save(data) #this query sends back a user id that we are storing in session
    return redirect("/welcome")

#LOGIN ROUTE

@app.route('/login', methods=['POST'])
def login():
    
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    
    if not user_in_db:
        flash("Invalid Email/Password", 'log')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", 'log')
        return redirect('/')
    
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['user_level'] = user_in_db.user_level #store admin value
    # never render on a post!!!
    return redirect("/welcome")
 
#ADMIN DASHBOARD ROUTE

@app.route('/admin/dashboard')
def dashboard():
  
    if not 'user_id' in session:
        return redirect('/welcome')
    if not session['user_level'] == '1':
        return 'YOU ARE NOT A ADMIN'
    all_orders = Order.get_all()
    revenue = Order.sum_amount()

    return render_template('admin_dashboard.html', all_orders = all_orders, revenue = revenue)




#LOGOUT ROUTE
@app.route('/logout')
def logout():
    del session['user_id']
   
    return redirect('/')