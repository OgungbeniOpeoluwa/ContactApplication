class UserExistException(Exception):
    pass


class InvalidLoginDetails(ValueError):
    pass

class AppLockedException(ValueError):
    pass
