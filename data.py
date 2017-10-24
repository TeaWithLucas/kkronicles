
from classes import *
import sql

def void():
	pass

game_title = 'Kirill Kronicles'

bitcoin_values = [{'name':'bitcoin', 'value':10**8, 'symbol':'₿'}, {'name':'milli', 'value':10**5, 'symbol':'m₿'}, {'name':'micro', 'value':10**2, 'symbol':'µ₿'}, {'name':'nano', 'value':1, 'symbol':'n₿'}]

#Pulls data form a BD table and integrates it into a class
def table_to_class(table, dic):
	stringSQL = "SELECT * FROM " + table + ";" #Create query
	tabledata = sql.fetch_all(stringSQL) #Fetch data form table
	outputdata = {} #Create dictionary for output
	#Put data into class object
	for row in tabledata:
		classobj = dic['class'](row)
		outputdata[classobj.id] = classobj
		print ("creating: " + classobj.id)
	return outputdata

#Pulling data from DB
actors = table_to_class("tblCharacters", {'class' : Actor})
locations = table_to_class("tblLocations", {'class' : Location})

#Items
book_item = Item('Book', 'an old book', 'This is a very old looking book.')
gun_item = Item('Gun', 'a shiny gun', 'This is a very reliable weapon.')

#Characters
#char_narrator = Actor('narrator_tag', '#D3D3D3', "Narrator")
#example_guy = Actor('sec_char_tag','#C1CDCD','Mr Hodge Hodgeson')


#Create the locations
#loc_menu = Location('menu','Menu', 'chem.bmp', '')
#loc_chem = Location('chem', 'Chemistry Labs', 'chem.bmp', 'You enter a long hall with various portraits on the walls.')
#loc_cliffs = Location('cliffs', 'Three Cliffs Bay', 'cliffs.bmp', 'You enter the main reception of the building. The room is empty.')
#loc_home = Location('home', 'Senghenydd Home', 'home.bmp', 'You step into a well iluminated office with a paintig of a snowy landscape on the wall.')
#loc_library = Location('library', 'Cathays Library', 'library.bmp','Before you is a busy cafe. The barista is strugling to keep up with the work load and looks at you desperately as you walk in.')
#loc_park = Location('park', 'Cathays Park', 'park.bmp', 'Before you is a busy cafe. The barista is strugling to keep up with the work load and looks at you desperately as you walk in.')
#loc_queens = Location('queens', 'Queens Buildings', 'queens.bmp', 'Before you is a busy cafe. The barista is strugling to keep up with the work load and looks at you desperately as you walk in.')
#loc_taf = Location('taf', 'The Taf Pubqueens', 'taf.bmp', 'Before you is a busy cafe. The barista is strugling to keep up with the work load and looks at you desperately as you walk in.')
#loc_triad = Location('triad', 'Wu\'s Won Now Casino & Noodle Bar', 'triad.bmp', 'Before you is a busy cafe. The barista is strugling to keep up with the work load and looks at you desperately as you walk in.')
#Stages

#Stages(integrate with DB in future)
stg_main_menu = Stage('main_menu', 'Main Menu', [{'speaker':actors['Nikeen_Patel'], 'dialog':(draw_ascii('./assets/welcome.txt') + '\n\n\n\n\n' + 'Welcome  Kirill\t'), 'location': locations['menu']}], {'start': 'wake_up', 'exit':'main_menu'}, 'narrated')
stg_wake_up = Stage('wake_up', 'Wake up', [{'speaker':actors['Nikeen_Patel'], 'dialog': 'You wake on your desk. Having worked late last night to complete your proposal to obtain funding for a start-up of your completely original and not and all copyright infringing program called CloudNet, a friendly security system.', 'location':locations['menu']}], {'continue': 'stat_menu'}, 'narrated' , 'act1')
stg_stat_menu = Stage('stat_menu', 'Stat Selection', [{'speaker':actors['Nikeen_Patel'], 'dialog':'', 'location': locations['menu']}], {'':''}, 'functional', 'select_stats', 'act1')
stg_act1 = Stage('act1', 'Act 1', [
	{'speaker':actors['Nikeen_Patel'], 'dialog':'You take your application to your superiors, moving through the many corridors of the Computer Science department. When you arrive, the head of the department looks over your proposal with one eyebrow raised. He turns his focus to you. ', 'location': locations['menu']},
	{'speaker':actors['Stuart_Allen'], 'dialog':'There is absolutely nothing you can say or do to make me give the green light to fund this kind of crazy program. An AI system as advanced as this could wipe out humanity completely....This program seems oddly familiar to one I have seen in a film before', 'location':  locations['menu']},
	{'speaker':actors['Nikeen_Patel'], 'dialog':'You leave the building with your head hanging low, you feel as though years of your work have gone to waste.\n Switch leaning on the wall with one leg propped up looks over from under his hood. ', 'location':  locations['menu']},
	{'speaker':actors['James_Wills'], 'dialog':'You look down, My G, Ive got some friends at the Taf who could cheer you up. Name s Switch', 'location':  locations['menu']},
	{'speaker':actors['Nikeen_Patel'], 'dialog':'You follow Switch. ', 'location':  locations['menu']}],  {'continue': 'main_menu'}, 'narrated')
stg_other_menu = Stage('other menu', 'other menu', [{'speaker':actors['Nikeen_Patel'], 'dialog':'Welcome  Krill', 'location': locations['menu']}],  {'start': 'act1', 'exit':'main_menu'},'narrated')
stg_new_game = Stage('new game', 'new game', [{'speaker':actors['Nikeen_Patel'], 'dialog':'Welcome  Krill', 'location': locations['menu']}],  {'start': 'act1', 'exit':'main_menu'}, 'narrated')
stg_load_game = Stage('load game', 'load game', [{'speaker':actors['Nikeen_Patel'], 'dialog':'Welcome  Krill', 'location': locations['menu']}],  {'start': 'act1', 'exit':'main_menu'}, 'narrated')
stg_exit = Stage('exit', 'Exiting', [{'speaker':actors['Nikeen_Patel'], 'dialog':'Welcome  Krill', 'location': locations['menu']}],  {'start': 'act1', 'exit':'main_menu'}, 'narrated')
stg_lost = Stage('lost', 'You Loose', [{'speaker':actors['Nikeen_Patel'], 'dialog':'You lost', 'location': locations['menu']}],  {'start': 'act1', 'exit':'main_menu'}, 'narrated')

stages = [stg_main_menu, stg_stat_menu, stg_act1, stg_other_menu, stg_new_game, stg_load_game, stg_exit, stg_lost, stg_wake_up]

item_names = []
#for item in global_game_items:
	#item_names.append(item.id)

directions = ['north', 'south', 'east', 'west']
action_cmds = ['move', 'take', 'drop']

directions = ['north', 'south', 'east', 'west']
action_cmds = ['move', 'take', 'drop']

keep_words = action_cmds + directions + item_names
