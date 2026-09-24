class ApplicationError(Exception):
    status_code = 500

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class ResourceNotFoundError(ApplicationError):
    status_code = 404


class ValidationError(ApplicationError):
    status_code = 400


class ConflictError(ApplicationError):
    status_code = 409


class DatabaseUnavailableError(ApplicationError):
    status_code = 503
