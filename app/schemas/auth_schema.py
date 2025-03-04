from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjk2MzQ2MzQ1fQ.OQEwjUNbvJKTR-ejdgSkgJT1BiZG4N-kTPX9zqgMKEQ",
                "token_type": "bearer"
            },
            "description": "Authentication token response that contains the JWT token to be used in subsequent API calls"
        }
    }

