from google.oauth2 import id_token
from google.auth.transport import requests
import os
from typing import Any


class GoogleOAuthService:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    def verify_google_token(self, token: str) -> dict[str, Any]:
        """
        Верифікує Google JWT токен

        Args:
            token: Google ID токен від фронтенду

        Returns:
            Словник з інформацією про користувача або помилкою
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.client_id
            )

            # Перевіряємо що токен від Google
            if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                return {
                    "status": "error",
                    "message": "Invalid token issuer"
                }

            return {
                "status": "success",
                "email": idinfo.get("email"),
                "name": idinfo.get("name"),
                "picture": idinfo.get("picture"),
                "google_id": idinfo.get("sub"),  # унікальний ID від Google
            }

        except ValueError as e:
            return {
                "status": "error",
                "message": f"Invalid token: {str(e)}"
            }