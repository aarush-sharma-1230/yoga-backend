from fastapi import HTTPException, status


class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class CustomException(Exception):
    def __init__(self, name: str = "Internal Server Error"):
        self.name = name


class SessionException(Exception):
    def __init__(self, name: str = "Session Error", type: str = "session"):
        self.name = name
        self.type = type


class QueryException(Exception):
    def __init__(self, name: str = "Query Error", type: str = "query"):
        self.name = name
        self.type = type
