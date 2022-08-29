import pymysql.cursors
import base64

host_name = "127.0.0.1"
user_name = "dltrhizm"
password_str = "RzbFrATtI0fE"

transfer_db = "dltrhizm_img-transfer"
record_db = "dltrhizm_record"
statistic_db = "dltrhizm_statistic"
trash_db = "dltrhizm_trash_status"

def update_log(classifier_name, image, confidence, category, sub_category, classify_date):
	connection = pymysql.connect(
			host = host_name,
			user = user_name,
			password = password_str,
			db = record_db,
			port = 3306,
			charset='utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		#cursor.execute("INSERT INTO `log` (`classifier`, `image`, `confidence`, `category`, `sub_category`, `date`) VALUES (%s,%s,%s,%s,%s,%s)",(classifier_name,image,confidence,category,sub_category,classify_date))
		sql = "INSERT INTO `log` (`classifier`, `image`, `confidence`, `category`, `sub_category`, `date`) VALUES (\'" + classifier_name + "\',\'" + image + "\',\'" + confidence + "\',\'" + category + "\',\'" + sub_category + "\',\'" + classify_date + "\')"
		cursor.execute(sql,)
	connection.commit()
	connection.close()
	# print(image)
	print("Update Complete")

def get_record(category, sub_category):
	# print("get",category,sub_category)
	connection = pymysql.connect(
			host = host_name,
			user = user_name,
			password = password_str,
			db = statistic_db,
			port = 3306,
			charset='utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		sql = "SELECT `Amount` FROM " + category + " WHERE `Type` = \'" + sub_category + "\'"
		cursor.execute(sql,)
		result = cursor.fetchone()
	connection.close()
	return result['Amount']

def update_record(category, sub_category):
	current = get_record(category, sub_category) + 1
	# print("get",category,sub_category)
	connection = pymysql.connect(
			host = host_name,
			user = user_name,
			password = password_str,
			db = statistic_db,
			port = 3306,
			charset='utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		#cursor.execute("INSERT INTO `log` (`classifier`, `image`, `confidence`, `category`, `sub_category`, `date`) VALUES (%s,%s,%s,%s,%s,%s)",(classifier_name,image,confidence,category,sub_category,classify_date))
		sql = "UPDATE `" + category + "` SET `Amount` = " + str(current) + " WHERE `Type` = \'" + sub_category + "\'"
		cursor.execute(sql,)
	connection.commit()
	connection.close()
	# print(image)
	print("Update Record Complete")

# def reset_trash():
# 	categories = ['Danger','General','Organic','Recycle']
# 	for types in category:	
# 		connection = pymysql.connect(
# 				host = host_name,
# 				user = user_name,
# 				password = password_str,
# 				db = trash_db,
# 				port = 3306,
# 				charset='utf8mb4',
# 				cursorclass = pymysql.cursors.DictCursor)
# 		with connection.cursor() as cursor:
# 			sql = "UPDATE `" + types + "` SET `Amount` = 0"
# 			cursor.execute(sql,)
# 		connection.commit()
# 		connection.close()

# def get_trash(category,sub_category):	
# 	# print("get",category,sub_category)
# 	connection = pymysql.connect(
# 			host = host_name,
# 			user = user_name,
# 			password = password_str,
# 			db = trash_db,
# 			port = 3306,
# 			charset='utf8mb4',
# 			cursorclass = pymysql.cursors.DictCursor)
# 	with connection.cursor() as cursor:
# 		sql = "SELECT `Amount` FROM `" + category + "` WHERE `Type` = \'" + sub_category + "\'"
# 		cursor.execute(sql,)
# 		result = cursor.fetchone()
# 	connection.close()
# 	return result['Amount']

def update_trash(category,sub_category,value):
	# current = get_trash(category,sub_category) + 1
	# print("get",category,sub_category)
	connection = pymysql.connect(
			host = host_name,
			user = user_name,
			password = password_str,
			db = trash_db,
			port = 3306,
			charset='utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		sql = "UPDATE `" + category + "` SET `Amount` = " + str(value) + " WHERE `Type` = \'" + sub_category + "\'"
		cursor.execute(sql,)
	connection.commit()
	connection.close()

update_trash('Recycle','Metal',64)