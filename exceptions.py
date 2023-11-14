class AttributeNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class AttributeAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class AttributeWrongType(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidAttributeType(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserHasNoAttribute(Exception):
    def __init__(self, message):
        super().__init__(message)


class PolicyAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidPolicyConditions(Exception):
    def __init__(self, message):
        super().__init__(message)


class ResourceAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class PolicyNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidResource(Exception):
    def __init__(self, message):
        super().__init__(message)


class ResourceNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
