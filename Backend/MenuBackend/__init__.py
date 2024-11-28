import MySQLdb
from django.conf import settings


def check_mysql_connection():
    try:
        connection = MySQLdb.connect(
            host=settings.DATABASES["default"]["HOST"],
            user=settings.DATABASES["default"]["USER"],
            passwd=settings.DATABASES["default"]["PASSWORD"],
            db=settings.DATABASES["default"]["NAME"],
            port=int(settings.DATABASES["default"]["PORT"]),
        )
        connection.close()
        return True
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return False
