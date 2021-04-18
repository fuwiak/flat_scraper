"""
pg_dump -h localhost -U postgres flats_database > backup.pgsql
"""
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from datetime import datetime


def main():
	gauth = GoogleAuth()
	gauth.LoadCredentialsFile("mycreds.txt")

	if gauth.credentials is None:
		gauth.LocalWebserverAuth()
	elif gauth.access_token_expired:
		gauth.Refresh()
	else:
		gauth.Authorize()

	drive = GoogleDrive(gauth)

	today = datetime.today().strftime('%d%B%Y')

	f = drive.CreateFile({'title': f"flats_db_{today}"})
	f.SetContentFile("backup.pgsql")
	f.Upload()
	f = None

	print("Uploaded")


if __name__ == '__main__':
	main()
