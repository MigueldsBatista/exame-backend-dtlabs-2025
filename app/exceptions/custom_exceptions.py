class ConflictException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnauthorizedException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)