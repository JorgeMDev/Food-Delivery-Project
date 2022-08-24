from flashk_app import app
from flask import render_template,redirect,request,session,flash
from flashk_app.models.user_model import User
from flashk_app.models.order_model import Order 
from flashk_app.models.menu_model import Menu

#ROUTE TO UPDATE CHANGE DE MENUS
@app.route('/menu/<int:id>/update')
def updatemenu(id):
    if not 'user_id' in session:
        return redirect('/')
    print('Menu Update')
    data = { 'id': id}

    user_id = {
        'id': session['user_id']
    }
 
    user_by_id = User.get_by_id(user_id)
    one_menu = Menu.get_by_id(data)

    
    return render_template('welcome.html', one_menu = one_menu, user_by_id = user_by_id)