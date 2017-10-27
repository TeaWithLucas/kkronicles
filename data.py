from classes import *
import sql

game_title = 'Kirill Kronicles'
email_z = Email('z', 'Yo Kirill', "You don’t know me, G, but I can hook you up with my product, you feel. If you want 'em. They'll be waiting at Cathays Park. Leave the money, my bredrin' will collect it. ")
email_d = Email('dmytro', 'spam', "I will send you a very big amount of spam emails if you sell drugs. ")
email_t = Email('white tiger', 'hello kirill', "I know you have been dealing for Castellano, but I want you to working for me. I can supply at less than he can. If you wish to join me, come to the Casino. ")
bitcoin_values = [{'name':'bitcoin', 'value':10**8, 'symbol':'B'}, {'name':'milli', 'value':10**5, 'symbol':'mB'}, {'name':'micro', 'value':10**2, 'symbol':'µB'}, {'name':'nano', 'value':1, 'symbol':'nB'}]

#Pulls data form a BD table and integrates it into a class
def table_to_class(table, dic):
	stringSQL = "SELECT * FROM " + table + ";" #Create query
	tabledata = sql.fetch_all(stringSQL) #Fetch data form table
	outputdata = {} #Create dictionary for output
	#Put data into class object
	print ("\nInitalising " + str(dic['class']))
	for row in tabledata:
		classobj = dic['class'](row)
		outputdata[classobj.id] = classobj
		print ("ID: " + classobj.id, end=", ")
	return outputdata

def table_to_list(table, id_name, id_value):
	stringSQL = "SELECT * FROM " + table + " WHERE " + id_name + " = '" + id_value + "';" #Create query
	tabledata = sql.fetch_all(stringSQL) #Fetch data form table
	outputdata = [] #Create list for output

	#complie narrarion into list
	for row in tabledata:
		outputdata.append(row)
	return outputdata

#Pulling data from DB
def reload_data():
	actors = table_to_class("kk_Actors", {'class' : Actor})
	locations = table_to_class("kk_Locations", {'class' : Location})
	items = table_to_class("kk_Items", {'class': Item})
	all_stages = table_to_class("kk_Stages", {'class': Stage})
	for stage in all_stages.values():
		stage.narration_add(table_to_list("kk_Narration", "stages_id", stage.id))
	recipes = table_to_class("kk_Recipes", {'class': Recipe})

actors = table_to_class("kk_Actors", {'class' : Actor})
locations = table_to_class("kk_Locations", {'class' : Location})
items = table_to_class("kk_Items", {'class': Item})
all_stages = table_to_class("kk_Stages", {'class': Stage})
for stage in all_stages.values():
	stage.narration_add(table_to_list("kk_Narration", "stages_id", stage.id))
recipes = table_to_class("kk_Recipes", {'class': Recipe})