import builtins
from classes.exception.ValidationException import ValidationException
import test.classes.Const as const
class UserFilter:

    BAD_USER_ID = 'watwatwat'

    def __init__ (self):
        pass

    def set_user_id (self, req):
        try:
            if builtins.db_fail == 'True':
                raise ValidationException('mock exception')
        except ValidationException as e:
            raise # coding=utf-8
        except Exception:
            pass

        req.cookies['user_id'] = const.GOOD_USER_ID
        print('the req:', req)
        print('the req json body:', req.json_body)
        print('the req cookies:', req.cookies)
        return req
