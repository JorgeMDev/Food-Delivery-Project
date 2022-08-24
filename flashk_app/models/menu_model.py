from flashk_app.config.mysqlconnection import connectToMySQL
from flashk_app import DATABASE, app
from flashk_app.models import user_model
from flask import flash, request

class Menu:
    def __init__(self,data):
        self.id = data['id']
        self.monday = data['monday']
        self.tuesday = data['tuesday']
        self.wednesday = data['wednesday']
        self.thursday = data['thursday']
        self.friday = data['friday']
        self.saturday = data['saturday']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.monday_url = data['monday_url']
        self.tuesday_url = data['tuesday_url']
        self.wednesday_url = data['wednesday_url']
        self.thursday_url = data['thursday_url']
        self.friday_url = data['friday_url']
        self.saturday_url = data['saturday_url']


    @classmethod
    def update(cls,data):
        query = "UPDATE menus SET monday = %(monday)s, tuesday = %(tuesday)s, wednesday = %(wednesday)s, thursday = %(thursday)s, friday = %(friday)s WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM menus;"
        result = connectToMySQL(DATABASE).query_db(query)
        # Didn't find a matching user
   
        return result
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM menus WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])