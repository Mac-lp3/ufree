import builtins
from classes.exception.ValidationException import ValidationException
class UserFilter:

    def __init__ (self):
        pass

    def set_user_id (self, req_body):
        if builtins.db_fail == 'True':
            raise ValidationException('mock exception')
        req_body['id'] = 'heyheyhey'
        return req_body
