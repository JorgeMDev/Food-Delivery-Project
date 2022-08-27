
from flashk_app import app
from flask import render_template,redirect,request,session,flash
from flashk_app.models.user_model import User
from flashk_app.models.order_model import Order 
from flashk_app.models.menu_model import Menu



#ROUTE TO CREATE ORDER
@app.route('/create/<int:id>/order')
def createorder(id):
    if not 'user_id' in session:
        return redirect('/')
    data = {'id' : session['user_id']}
    menuid = {'id': id}
    menu_by_id = Menu.get_by_id(menuid)
    user_by_id = User.get_by_id(data)  
    return render_template('add_order.html', user_by_id = user_by_id, menu_by_id = menu_by_id)

#ROUTE AFTER ORDER HAS BEEN PLACED
@app.route('/add/order', methods=['POST'])
def addorder():
    if not 'user_id' in session: 
        return redirect('/')
    if not Order.validator(request.form): 
        return redirect('/create/order')
    data = {
        **request.form,
        'user_id': session['user_id']   
    }
    Order.save(data)
    return redirect('/welcome')

#SAVE FORM INFO IN DATABASE AS A NEW ORDER
@app.route('/order/placed', methods=['POST'])
def orderplaced():
    print(request.form)
    menu_id = request.form['menu_id']
    print(menu_id)
    if not 'user_id' in session: 
        return redirect('/')
    if not User.validate_user_order(request.form): 
        return redirect(f'/create/{menu_id}/order')
    order_data = {
        'status' : 'pending',
        'user_id': session['user_id'], 
        'menu_id': menu_id,
        'amount': '59.99',
        'description': request.form['description']
    }

    user_data = {
        'id' : session['user_id'],
        'address': request.form['address'],
        'phone': request.form['phone']
    }

    receiver = request.form['email']

    User.email_to_user(receiver)
    User.update(user_data)
    Order.save(order_data)   
    return redirect('/message')

#DISPLAY MESSAGE :ORDER HAS BEEN PLACED!
@app.route('/message')
def message():
    if not 'user_id' in session: 
        return redirect('/')
    return render_template('message.html')

#UPDATE ORDER
@app.route('/update/<int:id>/order')
def update(id):
    data = {
        'id':id,
        'status':'Delivered'
    }

    Order.update(data)
    return redirect('/admin/dashboard')

#CANCEL ORDER
@app.route('/delete/<int:id>/order')
def cancel(id):
    data = {
        'id':id,
        'status':'Cancelled'
    }

    Order.update(data)
    return redirect('/admin/dashboard')
