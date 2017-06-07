import builtins
from classes.exception.ValidationException import ValidationException
class UserFilter:

    def __init__ (self):
        pass

    def set_user_id (self, req):
        if builtins.db_fail == 'True':
            raise ValidationException('mock exception')
        req.cookies['user_id'] = 'heyheyhey'
        print('the req:', req)
        print('the req json body:', req.json_body)
        print('the req cookies:', req.cookies)
        return req
