from ftplib import all_errors
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = "methane"


class User: 
    def __init__(self, data):
        #add attributes per column in table
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

#create class method to save the users into database
    @classmethod
    def create(cls,data:dict) -> int:
        #add all column names and all values
        query = "INSERT INTO users (first_name, last_name, email, pw) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(pw)s);"
        #returns me the id/ row of new user added to database
        user_id = connectToMySQL(DATABASE).query_db(query,data)
        return user_id


#selecting user by id
    @classmethod
    def get_one(cls,data:dict) -> int:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False

#selecting user by id
    @classmethod
    def get_one_by_email(cls,data:dict) -> int:
        query = "SELECT * FROM users WHERE email= %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False

#appending users into the table
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return False

    @classmethod
    def update_one(cls,data:dict) -> None:
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WEHRE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def delete_one(cls, data:dict) -> None:
        #add columns = values for every column you want to change
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


#statiic method for checking if user is valid to register
    @staticmethod
    def validator(data:dict) -> bool:
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters.", "err_users_first_name")
            is_valid = False

        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters.", "err_users_last_name")
            is_valid = False

        if len(data['email']) < 1 :
            flash("Password must be at least 8 characters.", "err_users_email")
            #the err will direct the error message on template

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email", "err_users_email")
            is_valid = False
            #cheking if email already in use
        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if potential_user:
                flash("Email already in use", "err_users_email")
                is_valid = False

        if len(data['pw']) < 3:
            flash("First name must be at least 3 characters.", "err_users_pw")
            is_valid = False

        if len(data['confirm_pw']) < 3:
            flash("First name must be at least 3 characters.", "err_users_confirm_pw")
            is_valid = False
        elif data['pw'] != data['confirm_pw']:
            flash("Passwords do not match.", "err_users_pw")

        return is_valid


#statiic method for checking if user is valid to login
    @staticmethod
    def validator_login(data:dict) -> bool:
        
        is_valid = True

        if len(data['email']) < 1 :
            flash("Password must be at least 8 characters.", "err_users_email_login")
            #the err will direct the error message on template

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email", "err_users_email_login")
            is_valid = False
            #cheking if email already in use
        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            print(potential_user.first_name)
            if not potential_user:
                flash("invalid credentials!", "err_users_email_login")
                is_valid = False
            #check the hash
            elif not bcrypt.check_password_hash(potential_user.pw, data['pw']):
                flash("invalid credentials!!", "err_users_email_login")
                is_valid = False
            else:
            #store id into session
                session['uuid'] = potential_user.id

        if len(data['pw']) < 3:
            flash("First name must be at least 3 characters", "err_users_pw_login")
            is_valid = False

        return is_valid