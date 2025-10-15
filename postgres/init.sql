ALTER TABLE public.job_entry ADD COLUMN search_vector tsvector;
CREATE INDEX idx_job_entry_search_vector ON public.job_entry USING GIN(search_vector);

CREATE OR REPLACE FUNCTION jobs_search_vector_update() RETURNS trigger AS $$
BEGIN
	UPDATE job_entry SET search_vector = to_tsvector('english', NEW.job_description || ' ' || NEW.experience || ' ' || NEW.skills || ' ' || NEW.responsibilities || ' ' || (tags::TEXT))
	WHERE id = NEW.id;

	RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_search_vector_update BEFORE INSERT OR UPDATE
ON job_detail FOR EACH ROW EXECUTE FUNCTION jobs_search_vector_update();

