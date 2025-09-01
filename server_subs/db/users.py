from server_subs.db import Database, db


class UserService:
    def __init__(self, database: Database):
        self.database = database
        self.UserModel = db.get_model('users')


user_service = UserService(db)
