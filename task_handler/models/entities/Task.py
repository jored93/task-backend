from utils.DateFormat import DateFormat


class Task():

    def __init__(self, id, name=None, description=None, user_id=None, status=False, created_at=None) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.status = status
        self.created_at = created_at

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': DateFormat.convert_date(self.created_at)
        }