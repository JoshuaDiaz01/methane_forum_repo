from ftplib import all_errors
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_user
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = "methane"


class Thought: 
    def __init__(self, data):
        #add attributes per column in table
        self.id = data['id']
        self.credential = data['credential']
        self.comment = data['comment']
        self.related_article = data['related_article']
        self.hypothesis = data['hypothesis']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.player = {}

#create class method to save the Instrument into database
    @classmethod
    def create(cls,data:dict) -> int:
        #add all column names and all values
        query = "INSERT INTO thoughts (comment, credential, related_article, hypothesis, date, user_id) VALUES (%(comment)s, %(credential)s,%(related_article)s,%(hypothesis)s,%(date)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)



#selecting user by id to route in the view thought (shows the user that posted)
    @classmethod
    def get_one(cls,data:dict) -> int:
        query = "SELECT * FROM thoughts JOIN users ON users.id = thoughts.user_id WHERE thoughts.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        dict = results[0]
        thought = cls(dict)
        user_data = {
            "id" : dict['users.id'],
            "first_name": dict['first_name'],
            "last_name": dict['last_name'], 
            "email": dict['email'],
            "pw": dict['pw'],
            'created_at': dict['users.created_at'],
            'updated_at': dict['users.updated_at'],
        }
        new_user = model_user.User(user_data)
        thought.player = new_user
        return thought



#appending thoughts into the table
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM thoughts JOIN users ON users.id = thoughts.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_thoughts = []
            for dict in results:
                thought = cls(dict)
                user_data = {
                    'id': dict['users.id'],
                    'created_at': dict['users.created_at'],
                    'updated_at': dict['users.updated_at'],
                    'first_name': dict['first_name'],
                    'last_name': dict['last_name'],
                    'email': dict['email'],
                    'pw': dict['pw'],
                }
                user = model_user.User(user_data)
                thought.player = user
                all_thoughts.append(thought)
            return all_thoughts
        return [] 

    @classmethod
    def update_one(cls, data:dict) -> None:
        #add columns = values for every column you want to change
        query = "UPDATE thoughts SET comment = %(comment)s, credential = %(credential)s,related_article = %(related_article)s,hypothesis = %(hypothesis)s,date = %(date)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one(cls,data:dict):
        query = "DELETE FROM thoughts WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


#statiic method for checking if instrument is valid to register
    @staticmethod
    def validator(data:dict) -> bool:
        is_valid = True
        if len(data['comment']) < 3:
            flash("Year(s) Analyzed must be at least 3 characters.", "err_thoughts_comment")
            is_valid = False

        # #name didnt match time_played
        # if len(data['credential']) < 1:
        #     flash("Time Played must be at least 3 characters.", "err_thoughts_credential")
        #     is_valid = False
    
        if len(data['related_article']) < 3:
            flash("Related Article must be at least 3 characters.", "err_thoughts_related_article")
            is_valid = False
        
        if len(data['hypothesis']) < 3:
            flash("Hypothesis must be at least 3 characters.", "err_thoughts_hypothesis")
            is_valid = False

        if len(data['date']) < 3:
            flash("Date must be updated.", "err_thoughts_date")
            is_valid = False
        
        return is_valid
    
    