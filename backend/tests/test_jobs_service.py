import pytest
from uuid import uuid4
from src.jobs import service as jobs_service
from src.exceptions import JobNotFoundError
from src.jobs.models import JobCreate

class TestJobsService:
    def test_create_job(self, db_session, test_token_data):
        job_create = JobCreate(
            job_title="New Job",
            job_description="New Description",
            responsibilities="Responsibilities",
            skills="Skills",
            benefits="Benefits",
            remote=True,
            location="Location",
            employment_type="FULL_TIME",
            created_at=None,
            updated_at=None
        )

        new_job = jobs_service.create_job(test_token_data, db_session, job_create)
        assert new_job.job_description == "New Description"
        assert new_job.responsibilities == "Responsibilities"
        assert new_job.skills == "Skills"
        assert new_job.benefits == "Benefits"
        assert new_job.remote is True
        assert new_job.location == "Location"
        assert new_job.employment_type == "FULL_TIME"
        assert new_job.created_at is not None
        assert new_job.updated_at is not None
        assert new_job.user_id == test_token_data.get_uuid()
        assert not new_job.is_completed

    def test_get_jobs(self, db_session, test_token_data, test_job):
        test_job.user_id = test_token_data.get_uuid()
        db_session.add(test_job)
        db_session.commit()

        jobs = jobs_service.get_jobs(test_token_data, db_session)
        assert len(jobs) == 1
        assert jobs[0].id == test_job.id

    def test_get_job_by_id(self, db_session, test_token_data, test_job):
        test_job.user_id = test_token_data.get_uuid()
        db_session.add(test_job)
        db_session.commit()

        job = jobs_service.get_job_by_id(test_token_data, db_session, test_job.id)
        assert job.id == test_job.id
        
        with pytest.raises(JobNotFoundError):
            jobs_service.get_job_by_id(test_token_data, db_session, uuid4())

    def test_complete_job(self, db_session, test_token_data, test_job):
        test_job.user_id = test_token_data.get_uuid()
        db_session.add(test_job)
        db_session.commit()

        completed_job = jobs_service.complete_job(test_token_data, db_session, test_job.id)
        assert completed_job.is_completed
        assert completed_job.completed_at is not None

    def test_delete_job(self, db_session, test_token_data, test_job):
        test_job.user_id = test_token_data.get_uuid()
        db_session.add(test_job)
        db_session.commit()

        jobs_service.delete_job(test_token_data, db_session, test_job.id)
        assert db_session.query(Job).filter_by(id=test_job.id).first() is None