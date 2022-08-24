from flashk_app.config.mysqlconnection import connectToMySQL
from flashk_app import DATABASE, app
from flask import flash
import re
import smtplib
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# User.py
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone = data['phone']
        self.address = data['address']
        self.password = data['password']
        self.user_level = data['user_level']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    def full_name(self):
        return f"{self.first_name} {self.last_name}"



    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        # comes back as the new row id
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])    

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])    

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET address = %(address)s, phone = %(phone)s WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result    

    # Static methods don't have self or cls passed into the parameters.
    # We do need to take in a parameter to represent our burger
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
                flash("First mame must be at least 2 character.", 'reg')
                is_valid = False
        if len(user['last_name']) < 2:
                flash("Last name must be at least 2 character.", 'reg')
                is_valid = False
        if len(user['email']) < 1:
                flash("Please provide a email.", 'reg')
                is_valid = False
        elif not EMAIL_REGEX.match(user['email']):   # if email does not match a proper format then send incorrect email message
                flash("Invalid email address!",'reg')
                is_valid = False
        else:
            data = {
                'email': user['email']
            }
            potencial_user= User.get_by_email(data) 
            if potencial_user:
                is_valid= False
                flash('Email already exist', 'reg') 
        if len(user['password']) < 8:
                flash("Password must be at least 8 characters.", 'reg')
                is_valid = False
        elif not user['password'] == user['password']:
                flash("Passwords don't match", 'reg')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_user_order(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
                flash("First mame must be at least 2 character.", 'ord')
                is_valid = False
        if len(user['last_name']) < 2:
                flash("Last name must be at least 2 character.", 'ord')
                is_valid = False
        if len(user['email']) < 1:
                flash("Please provide a email.", 'ord')
                is_valid = False
        if len(user['address']) < 1:
                flash("Please provide a address.", 'ord')
                is_valid = False
        if len(user['phone']) < 10:
                flash("Please provide a valid phone.", 'ord')
                is_valid = False
        return is_valid

   
    @staticmethod
    def email_to_user(receiver):
        try:
            x= smtplib.SMTP('smtp.gmail.com',587)
            x.starttls()
            x.login('jorgemartinez1990@gmail.com','uzyiyemfqwjymryb')
            subject='EatMoreHealthy: Order Placed'
            body_text='Thank you for choosing us! Your order is pending, we will let you know once it is proccesed and delivered!'
            message='Subject: {}\n\n{}'.format(subject,body_text)
            x.sendmail('jorgemartinez1990@gmail.com', receiver, message)
            print('Email sent')
        except Exception as exception:
            print(exception)
            print('Fail to sent')
    
    @staticmethod
    def admin(user):
        is_valid = True
        if not user['user_level'] == '1':
            is_valid = False
        return is_valid


   