
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ermira",
    port="3306",
    database="viya2022"
)

# ('admindrop_location',)
# ('auth_group',)
# ('auth_group_permissions',)
# ('auth_permission',)
# ('auth_user',)
# ('auth_user_groups',)
# ('auth_user_user_permissions',)
# ('django_admin_log',)
# ('django_content_type',)
# ('django_migrations',)
# ('django_session',)
# ('sellers',)
# ('viya1_address',)
# ('viya1_city',)
# ('viya1_contact',)
# ('viya1_district',)
# ('viya1_division',)
# ('viya1_property',)
# ('viya1_propertysingle',)
# ('viya1_status',)
# ('viya1_subdistrict',)
# ('viya1_type',)

mycursor = mydb.cursor()
mycursor.execute("Show tables;")
# myresult = mycursor.fetchall()
# mycursor.execute("show columns from viya1_property;")
#


myresult = mycursor.fetchall()

for x in myresult:
  print(x)