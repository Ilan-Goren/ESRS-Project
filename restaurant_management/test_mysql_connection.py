import MySQLdb

try:
    connection = MySQLdb.connect(
        host='localhost',
        user='your_mysql_user',
        passwd='your_mysql_password',
        db='restaurant_inventory'
    )
    print("Connection successful")
except MySQLdb.OperationalError as e:
    print(f"Connection failed: {e}")

