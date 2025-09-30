from fastapi import HTTPException

class JobError(HTTPException):
    """Base exception for job-related errors"""
    pass

class JobNotFoundError(JobError):
    def __init__(self, job_id=None):
        message = "Job not found" if job_id is None else f"Job with id {job_id} not found"
        super().__init__(status_code=404, detail=message)

class JobCreationError(JobError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create job: {error}")


class ProfileError(HTTPException):
    """Base exception for profile-related errors"""
    pass


class ProfileNotFoundError(ProfileError):
    def __init__(self, profile_id=None):
        message = "Profile not found" if profile_id is None else f"Profile with id {profile_id} not found"
        super().__init__(status_code=404, detail=message)

class ProfileNotAccessibleError(ProfileError):
    def __init__(self, profile_id=None):
        message = "Profile not accessible" if profile_id is None else f"Profile with id {profile_id} is not accessible"
        super().__init__(status_code=403, detail=message)

class UserError(HTTPException):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="New passwords do not match")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail="Current password is incorrect")

class EmailAlreadyExistsError(UserError):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"Email '{email}' is already registered")

class IdentificationAlreadyExistsError(UserError):
    def __init__(self, identification_number: str):
        super().__init__(status_code=400, detail=f"Identification number '{identification_number}' is already registered")

class CompanyRegistrationNumberExistsError(UserError):
    def __init__(self, registration_number: str):
        super().__init__(status_code=400, detail=f"Company registration number '{registration_number}' is already registered")

class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Could not validate user"):
        super().__init__(status_code=401, detail=message)

class AuthorizationError(HTTPException):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(status_code=403, detail=message)