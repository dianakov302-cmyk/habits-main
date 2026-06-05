from typing import Any
import bcrypt
from backend.repositories.user_repository import UserRepository
from backend.business_logic.services.interfaces import IUserService
from backend.domain.models.user import UserCreate, UserResponse

class UserService(IUserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login_user(self, email: str, password: str):
        try:
            user = self.user_repository.find_by_email(email)
            if not user:
                return {"status": "error", "message": "Identity not found. Please sign up."}

            stored_password = user.get("password", "")

            # Try bcrypt verification first
            password_ok = False
            try:
                password_ok = bcrypt.checkpw(password.encode(), stored_password.encode())
            except Exception:
                pass

            # Migration: if bcrypt fails but plaintext matches, rehash and save
            if not password_ok and stored_password == password:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                try:
                    self.user_repository.collection.update_one(
                        {"email": email},
                        {"$set": {"password": hashed}},
                    )
                except Exception:
                    pass
                password_ok = True

            if password_ok:
                return {"status": "success", "email": email, "message": "Login successful. Welcome back!"}

            return {"status": "error", "message": "Wrong password. Please try again."}
        except Exception as e:
            return {"status": "error", "message": f"Login failed: {str(e)}"}

    def logout_user(self, email: str):
        return {"status": "success", "message": "Logout successful. See you next time!"}

    def register_user(self, email: str, password: str, name: str | None = None):
        try:
            if self.user_repository.find_by_email(email):
                return {"status": "error", "message": "Email already registered. Please log in."}
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            self.user_repository.create_user({"email": email, "password": hashed, "name": name or ""})
            return {"status": "success", "message": "Registration successful. Welcome aboard!"}
        except Exception as e:
            return {"status": "error", "message": f"Registration failed: {str(e)}"}

    def save_test_result(
        self,
        session_id: str,
        answers: list[str],
        profile: dict[str, Any],
        roadmap: dict[str, Any],
        email: str | None = None,
    ) -> dict[str, Any]:
        try:
            storage = self.user_repository.save_quiz_result(
                {
                    "session_id": session_id,
                    "email": email,
                    "answers": answers,
                    "profile": profile,
                    "roadmap": roadmap,
                }
            )
            return {
                "status": "success",
                "message": "Test result saved.",
                "storage": storage,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to save test result: {str(e)}"}

    def get_user_profile(self, email: str):
        try:
            user = self.user_repository.collection.find_one(
                {"email": email},
                {"_id": 0, "password": 0},
            )
            if user:
                return {"status": "success", "data": user}
            return {"status": "error", "message": "User not found."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch profile: {str(e)}"}

    def update_user_profile(
        self,
        email: str,
        new_email: str = None,
        new_password: str = None,
        name: str | None = None,
        avatar_url: str | None = None,
        overview: str | None = None,
    ):
        try:
            update_fields = {}
            if new_email:
                update_fields["email"] = new_email
            if new_password:
                update_fields["password"] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            if name is not None:
                update_fields["name"] = name.strip()
            if avatar_url is not None:
                update_fields["avatar_url"] = avatar_url
            if overview is not None:
                update_fields["overview"] = overview.strip()
            if not update_fields:
                return {"status": "error", "message": "No updates provided."}
            result = self.user_repository.collection.update_one(
                {"email": email},
                {"$set": update_fields},
            )
            if result.matched_count == 0:
                return {"status": "error", "message": "User not found."}
            return {"status": "success", "message": "Profile updated successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update profile: {str(e)}"}

