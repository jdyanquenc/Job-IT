from sqlalchemy.orm import Session
from src.auth.models import TokenData
from src.companies.models import SearchCompanyResponse
from src.entities.company import Company


def get_resume_companies(current_user: TokenData, db: Session, query: str) -> list[SearchCompanyResponse]:
    companies = db.query(Company)
    if query:
        companies = companies.filter(Company.name.ilike(f"%{query}%"))
    companies = companies.limit(5).all()
    return [SearchCompanyResponse(
        id=company.id,
        name=company.name
    ) for company in companies]
