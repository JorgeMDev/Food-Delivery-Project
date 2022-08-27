from unittest import result
from flashk_app.config.mysqlconnection import connectToMySQL
from flashk_app import DATABASE, app
from flashk_app.models import user_model
from flask import flash, request

class Order:
    def __init__(self,data):
        self.id = data['id']
        self.description = data['description']
        self.status = data['status']
        self.amount = data['amount']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.menu_id = data['menu_id']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders JOIN users ON users.id = orders.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if results:
            all_orders = []
            for row in results:
                this_order = cls(row) 
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_order.customer = this_user
                all_orders.append(this_order) 
            return all_orders
        return results

    @classmethod
    def save(cls, data):
        print(data)
        query = "INSERT INTO orders (description,status,amount, user_id, menu_id) VALUES (%(description)s,%(status)s,%(amount)s,%(user_id)s,%(menu_id)s);"
        # comes back as the new row id
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def update(cls,data):
        query = "UPDATE orders SET status = %(status)s WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM orders WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

 
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM orders JOIN users ON users.id = orders.user_id WHERE orders.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        row = result[0]
        this_order = cls(row)
        user_data = {
            **row,
            'id': row['users.id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
          }
        user = user_model.User(user_data)
        this_order.customer = user
        return this_order

    @classmethod
    def sum_amount(cls):
        query  = "SELECT SUM(amount) FROM orders WHERE id > 0;"
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        return result[0]['SUM(amount)'] 
    
    @classmethod
    def pending_orders(cls):
        query  = "SELECT COUNT(id) FROM orders WHERE status = 'pending';"
        result = connectToMySQL(DATABASE).query_db(query)
        print(result)
        return result[0]['COUNT(id)'] 



    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['location']) < 1:
            flash("Location required")
            is_valid = False
        if len(form_data['what']) < 1:
            flash("Describe the event")
            is_valid = False
        if len(form_data['quantity']) < 1:
            flash("Number of Sasquatches required")
            is_valid = False
        if len(form_data['date']) < 1:
            flash("Date required")
            is_valid = False
        return is_valid