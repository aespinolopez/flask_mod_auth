class CustomError(Exception):
    """Base class for exceptions in this module"""
    pass


class ValidationError(CustomError):
    """Exception raised for input that not pass validation rules

    Attributes:
       field: field that has been validated
       errors: str list validation errors
    """
    def __init__(self, field: str, errors: list):
        self.errors = errors
        custom_message = '{field} has the following errors:\n{errors}'.format(field=field, errors=',\n'.join(errors))
        super().__init__(custom_message)


class ApiQueryError(CustomError):
    """Exception raised when invalid GET arguments are passed to the url
    Attributes:
       message: information about invalid arguments
    """
    def __init__(self, message: str):
        super().__init__(message)
