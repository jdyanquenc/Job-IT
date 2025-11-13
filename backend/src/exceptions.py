from fastapi import HTTPException


class BaseError(HTTPException):
    """Base exception for application errors"""
    def __init__(self, status_code: int, error_code: str, message: str):
        super().__init__(status_code=status_code, detail={"error_code": error_code, "message": message})

class JobError(BaseError):
    """Base exception for job-related errors"""
    pass

class JobNotFoundError(JobError):
    def __init__(self, job_id=None):
        error_code = "job_not_found"
        message = "Job not found" if job_id is None else f"Job with id {job_id} not found"
        super().__init__(status_code=404, error_code=error_code, message=message)

class JobCreationError(JobError):
    def __init__(self, error: str):
        error_code = "job_creation_failed"
        message = "Job creation failed" if error is None else f"Job creation failed: {error}"
        super().__init__(status_code=500, error_code=error_code, message=message)

class JobAccessError(JobError):
    def __init__(self, job_id=None):
        error_code = "job_access_forbidden"
        message = "Job access forbidden" if job_id is None else f"Access to job with id {job_id} is forbidden"
        super().__init__(status_code=403, error_code=error_code, message=message)

class JobAlreadyAppliedError(JobError):
    def __init__(self, job_id=None):
        error_code = "job_already_applied"
        message = "Job already applied" if job_id is None else f"Job with id {job_id} already applied"
        super().__init__(status_code=400, error_code=error_code, message=message)

class JobsRelatedError(JobError):
    def __init__(self, job_id=None):
        error_code = "related_jobs_error"
        message = "Error fetching related jobs" if job_id is None else f"Error fetching related jobs for job with id {job_id}"
        super().__init__(status_code=500, error_code=error_code, message=message)

class ProfileError(BaseError):
    """Base exception for profile-related errors"""
    pass

class ProfileNotFoundError(ProfileError):
    def __init__(self, profile_id=None):
        error_code = "profile_not_found"
        message = "Profile not found" if profile_id is None else f"Profile with id {profile_id} not found"
        super().__init__(status_code=404, error_code=error_code, message=message)

class ProfileNotAccessibleError(ProfileError):
    def __init__(self, profile_id=None):
        error_code = "profile_not_accessible"
        message = "Profile not accessible" if profile_id is None else f"Profile with id {profile_id} is not accessible"
        super().__init__(status_code=403, error_code=error_code, message=message)

class WorkExperienceFoundError(ProfileError):
    def __init__(self, experience_id=None):
        error_code = "work_experience_not_found"
        message = "Work experience not found" if experience_id is None else f"Work experience with id {experience_id} not found"
        super().__init__(status_code=404, error_code=error_code, message=message)

class WorkExperienceNotAccessibleError(ProfileError):
    def __init__(self, experience_id=None):
        error_code = "work_experience_not_accessible"
        message = "Work experience not accessible" if experience_id is None else f"Work experience with id {experience_id} is not accessible"
        super().__init__(status_code=403, error_code=error_code, message=message)

class WorkExperienceBadRequestError(ProfileError):
    def __init__(self, experience_id=None):
        error_code = "work_experience_bad_request"
        message = "Work experience bad request" if experience_id is None else f"Work experience with id {experience_id} bad request"
        super().__init__(status_code=400, error_code=error_code, message=message)


class EducationExperienceNotFoundError(ProfileError):
    def __init__(self, experience_id=None):
        error_code = "education_experience_not_found"
        message = "Education experience not found" if experience_id is None else f"Education experience with id {experience_id} not found"
        super().__init__(status_code=404, error_code=error_code, message=message)

class EducationExperienceNotAccessibleError(ProfileError):
    def __init__(self, experience_id=None):
        error_code = "education_experience_not_accessible"
        message = "Education experience not accessible" if experience_id is None else f"Education experience with id {experience_id} is not accessible"
        super().__init__(status_code=403, error_code=error_code, message=message)

class EducationExperienceBadRequestError(ProfileError):
    def __init__(self, experience_id=None):
        error_code = "education_experience_bad_request"
        message = "Education experience bad request" if experience_id is None else f"Education experience with id {experience_id} bad request"
        super().__init__(status_code=400, error_code=error_code, message=message)


class UserError(BaseError):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        error_code = "user_not_found"
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, error_code=error_code, message=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        error_code = "password_mismatch"
        message="New passwords do not match"
        super().__init__(status_code=400, error_code=error_code, message=message)

class InvalidPasswordError(UserError):
    def __init__(self):
        error_code = "invalid_password"
        message = "Current password is incorrect"
        super().__init__(status_code=401, error_code=error_code, message=message)

class EmailAlreadyExistsError(UserError):
    def __init__(self, email: str):
        error_code = "email_already_exists"
        message = f"Email '{email}' is already registered"
        super().__init__(status_code=400, error_code=error_code, message=message)

class IdentificationAlreadyExistsError(UserError):
    def __init__(self, identification_number: str):
        error_code = "identification_already_exists"
        message = f"Identification number '{identification_number}' is already registered"
        super().__init__(status_code=400, error_code=error_code, message=message)

class CompanyRegistrationNumberExistsError(UserError):
    def __init__(self, registration_number: str):
        error_code = "company_registration_number_exists"
        message = f"Company registration number '{registration_number}' is already registered"
        super().__init__(status_code=400, error_code=error_code, message=message)

class AuthenticationError(BaseError):
    def __init__(self, message: str = "Could not validate credentials"):
        error_code = "authentication_failed"
        super().__init__(status_code=401, error_code=error_code, message=message)

class AuthorizationError(BaseError):
    def __init__(self, message: str = "Access forbidden"):
        error_code = "authorization_failed"
        super().__init__(status_code=403, error_code=error_code, message=message)