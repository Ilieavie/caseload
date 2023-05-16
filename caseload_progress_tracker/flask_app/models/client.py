from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

#DONE

class Client:
    db = "project_db"
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.diagnosis = db_data['diagnosis']
        self.address = db_data['address']
        self.medications = db_data['medications']
        self.goals = db_data['goals']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.users_id = db_data['users_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM clients
                JOIN users on clients.users_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        clients = []
        for row in results:
            this_client = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "organization": row['organization'],
                "work_email": row['work_email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_client.creator = user.User(user_data)
            clients.append(this_client)
        return clients
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM clients
                JOIN users on clients.users_id = users.id
                WHERE clients.id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_client = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "organization": result['organization'],
                "work_email": result['work_email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_client.creator = user.User(user_data)
        return this_client

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO clients (first_name, last_name, diagnosis, goals, address, medications, users_id)
                VALUES (%(first_name)s,%(last_name)s,%(diagnosis)s, %(goals)s, %(address)s, %(medications)s, %(users_id)s);
                """
        return connectToMySQL(cls.db).query_db(query,form_data)
    
    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE clients SET first_name = %(first_name)s, last_name = %(last_name)s, diagnosis = %(diagnosis)s, goals = %(goals)s, address = %(address)s, medications = %(medications)s   WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM clients WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_client(form_data):
        is_valid = True

        if len(form_data['first_name']) < 3:
            flash("first_name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash("last_name must be at least 3 characters long.")
            is_valid = False
        if form_data['diagnosis'] == '':
            flash("Please input a diagnosis.")
            is_valid = False
        if form_data['goals'] == '':
            flash("Please input a goal.")
            is_valid = False  
        if form_data['address'] == '':
            flash("Please input an address.")
            is_valid = False  
        if form_data['medications'] == '':
            flash("Please input medications.")
            is_valid = False
        return is_valid


