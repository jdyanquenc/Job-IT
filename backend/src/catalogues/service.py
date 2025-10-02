from sqlalchemy.orm import Session
from src.auth.models import TokenData
from src.catalogues.models import SearchCompanyResponse, SearchInstitutionResponse
from src.entities.company import Company
from src.entities.educational_institution import EducationalInstitution


def get_resume_companies(current_user: TokenData, db: Session, query: str) -> list[SearchCompanyResponse]:
    companies = db.query(Company)
    if query:
        companies = companies.filter(Company.name.ilike(f"%{query}%"))
    companies = companies.limit(5).all()
    return [SearchCompanyResponse(
        id=company.id,
        name=company.name
    ) for company in companies]


def get_resume_institutions(current_user: TokenData, db: Session, query: str) -> list[SearchInstitutionResponse]:
    institutions = db.query(EducationalInstitution)
    if query:
        institutions = institutions.filter(EducationalInstitution.name.ilike(f"%{query}%"))
    institutions = institutions.limit(5).all()
    return [SearchInstitutionResponse(
        id=institution.id,
        name=institution.name
    ) for institution in institutions]