web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --keep-alive 2 --preload main:app
release: python -c "from app import app, db; app.app_context().push(); db.create_all()"