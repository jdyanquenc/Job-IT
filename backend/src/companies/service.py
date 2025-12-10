from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.entities.company import Company
from . import models
from src.auth.models import TokenData
from src.entities.todo import Todo
from src.exceptions import JobCreationError, JobNotFoundError
import logging

def create_company(current_user: TokenData, db: Session, company: models.CompanyCreate) -> Company:
    try:
        new_company = Company(**company.model_dump())
        new_company.user_id = current_user.get_uuid()
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        logging.info(f"Created new company for user: {current_user.get_uuid()}")
        return new_company
    except Exception as e:
        logging.error(f"Failed to create company for user {current_user.get_uuid()}. Error: {str(e)}")
        raise JobCreationError(str(e))


def get_companies(current_user: TokenData, db: Session) -> list[models.CompanyResponse]:
    companies = db.query(Company).filter(Company.user_id == current_user.get_uuid()).all()
    logging.info(f"Retrieved {len(companies)} companies for user: {current_user.get_uuid()}")
    return companies


def get_company_by_id(current_user: TokenData, db: Session, company_id: UUID) -> Company:
    company = db.query(Company).filter(Company.id == company_id).filter(Company.user_id == current_user.get_uuid()).first()
    if not company:
        logging.warning(f"Company {company_id} not found for user {current_user.get_uuid()}")
        raise JobNotFoundError(company_id)
    logging.info(f"Retrieved company {company_id} for user {current_user.get_uuid()}")
    return company


def update_company(current_user: TokenData, db: Session, company_id: UUID, company_update: models.CompanyCreate) -> Company:
    company_data = company_update.model_dump(exclude_unset=True)
    db.query(Company).filter(Company.id == company_id).filter(Company.user_id == current_user.get_uuid()).update(company_data)
    db.commit()
    logging.info(f"Successfully updated company {company_id} for user {current_user.get_uuid()}")
    return get_company_by_id(current_user, db, company_id)


def delete_company(current_user: TokenData, db: Session, company_id: UUID) -> None:
    company = get_company_by_id(current_user, db, company_id)
    db.delete(company)
    db.commit()
    logging.info(f"Company {company_id} deleted by user {current_user.get_uuid()}")
