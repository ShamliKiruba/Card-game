class User:
    def __init__(self):
        print("User class init function")
        self._session_id = None
        self._user_name = ''
        self._room = ''
    
    def set_session_id(self, id):
        self._session_id = id

    def get_session_id(self, id):
        return self._session_id

    def set_user_name(self, name):
        self._user_name = name
    
    def get_user_name(self):
        return self._user_name
    
    def set_room(self, room):
        self._room = room
    
    def get_room(self):
        return self._room