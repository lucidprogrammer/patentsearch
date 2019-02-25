CREATE TABLE IF NOT EXISTS brf_sum_text(
   uuid  SERIAL PRIMARY KEY,
   patent_id character varying(250) UNIQUE NOT NULL,
   text TEXT NOT NULL

);
-- comments which could make it easy to read from a viewer
COMMENT ON TABLE brf_sum_text IS 'Brief summary text';
COMMENT ON COLUMN brf_sum_text.uuid IS 'uuid as imported from patentsview csv';
COMMENT ON COLUMN brf_sum_text.patent_id IS 'Patent id';
COMMENT ON COLUMN brf_sum_text.text IS 'summary text';
