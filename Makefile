start:
	poetry run flask --app lesson5/example --debug run --port 8000

new_user:
	# poetry run flask --app lesson5/new_user --debug run --port 8000 --host /users
	# poetry run flask --app lesson5/users --debug run --port 8000
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 --chdir ./lesson5 users:app

