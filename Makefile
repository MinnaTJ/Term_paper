PY=python

init:
	@echo "Environment ready."

backfill:
	$(PY) src/ingest_news.py
	$(PY) src/ingest_tweets.py
	$(PY) src/ingest_complaints.py || true
	$(PY) src/get_olist.py

clean:
	$(PY) src/clean_textual.py
	$(PY) src/clean_structured.py

dict:
	$(PY) src/build_dictionary.py

all: backfill clean dict
	@echo "Phase 1 complete. See data/raw, data/clean, docs/, logs/."
