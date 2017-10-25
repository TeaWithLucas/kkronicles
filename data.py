from classes import *
import sql

game_title = 'Kirill Kronicles'

bitcoin_values = [{'name':'bitcoin', 'value':10**8, 'symbol':'₿'}, {'name':'milli', 'value':10**5, 'symbol':'m₿'}, {'name':'micro', 'value':10**2, 'symbol':'µ₿'}, {'name':'nano', 'value':1, 'symbol':'n₿'}]

#Emails
email_z = Email('z', 'Yo Kirill', "You don’t know me, G, but I can hook you up with my product, you feel. If you want 'em. They'll be waiting. Leave the money, my bredrin' will collect it. ")
email_d = Email('dmytro', 'spam', "I will send you a very big amount of spam emails if you sell drugs. ")
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
items = table_to_class("tblItems", {'class': Item})
recipes = table_to_class("tblRecipes", {'class': Recipe})

#Items
#book_item = Item('Book', 'an old book', 'This is a very old looking book.')
#gun_item = Item('Gun', 'a shiny gun', 'This is a very reliable weapon.')

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
stg_main_menu = Stage('stg_main_menu', 'Main Menu', [{'speaker':actors['Dmytro_Kaduba'], 'dialog':(draw_ascii('./assets/welcome.txt') + '\n\n\n\n\n' + '0Welcome  Kirill\t'), 'location': locations['menu']}], "What would you like to do?", {'Start': {'cmd':'cmd_change_scene', 'var':'stg_stat_choice'}, 'Exit':{'cmd':'cmd_exit', 'var':''}})

stg_stat_choice = Stage('stg_stat_choice', 'Selecting Stats', [{'speaker':actors['Nikeen_Patel'], 'dialog':'[APPLICATIION FORM]', 'location': locations['menu']}, {'speaker':actors['Dmytro_Kaduba'], 'dialog':'Enter your chosen stats to complete your application by typing the stat followed by the value. When you are done type [continue]. ', 'location': locations['menu']}], "What would you like to do?", {'continue': {'cmd':'cmd_change_scene', 'var':'stg_act1'},'open tor': {'cmd':'cmd_open_tor', 'var':'stg_act1'},'cook drug': {'cmd':'cmd_cook_menu', 'var':''}})
stg_act1 = Stage('stg_act1', 'Act 1', [
	{'speaker':actors['Nikeen_Patel'], 'dialog':'Lorem ipsum dolor sit amet, sea ei ridens signiferumque, vel no graece altera viderer. Has diam nibh no. Pro in noster probatus eleifend, saepe graecis corpora quo ei. Debitis definitiones quo ad, tollit eirmod patrioque ad vim, dico dolore assentior ut mel. Vel epicurei intellegam ex. Cum probatus theophrastus an, per id tota virtute.', 'location': locations['queens']},
	{'speaker':actors['James_Wills'], 'dialog':'Dico quando invidunt ei sit. Et bonorum delicata cum, per falli praesent explicari ea. Usu et tale error dissentiet, cum an laboramus aliquando repudiandae. Munere eloquentiam disputationi in vix. Tota salutandi rationibus eu pro, ius no persius menandri. Eam ut purto case instructior, decore periculis reprehendunt mei in, ea dicat cotidieque cum.', 'location':  locations['queens']},
	{'speaker':actors['Bai_Hu'], 'dialog':'Indoctum ocurreret cu duo, propriae deseruisse philosophia in est. Nam id tale timeam alienum, purto elaboraret qui no. At vim ferri labitur ceteros, nam eu dictas recteque intellegebat. Vis ea amet sumo, pro ex tacimates repudiare consetetur, id eos legimus omittam referrentur. Ne sea ludus voluptaria rationibus. Ad oratio consulatu aliquando ius, duo legere probatus et.', 'location':  locations['home']},
	{'speaker':actors['Kirill_Sidorov'], 'dialog':'Nisl postulant ne eos. Ut eos vide dolor urbanitas, ipsum legere instructior no eam. Quo eu affert recusabo partiendo, his ne accusam probatus facilisi. Soleat forensibus definiebas ex vix.', 'location':  locations['park']},
	{'speaker':actors['Nikeen_Patel'], 'dialog':'Porro graeco semper ei quo, per iudico percipit ut. Exerci luptatum elaboraret mel ex, no sed debet commodo dolores. Erat liber tantas at vis. Ut possit prompta feugiat nec, summo interesset an his, debitis probatus convenire id vix. Nobis dissentiunt sed ei, cum at impetus viderer definiebas. Ius cu nominavi mediocrem, an mel iriure dolorum, et veritus inciderint ius. Ad case virtute eleifend est.', 'location':  locations['park']},
	{'speaker':actors['William_Davies'], 'dialog':'Id eum dicunt ullamcorper, ne sea enim appareat. Omnium repudiare eu ius. Vero dicit sea te, mea ad iuvaret sensibus. Ex vis doming commodo theophrastus, prima civibus laboramus his cu. Ius ea soluta mollis erroribus, modus novum eu has.', 'location':  locations['home']}
	],  "What do you decide?", {'Yes': {'cmd':'cmd_change_scene', 'var':'stg_act1b'}, 'No':{'cmd':'cmd_dialog_choice', 'var':'no'}})
stg_act1b = Stage('stg_act1b', 'Act 1b', [{'speaker':actors['Kirill_Sidorov'], 'dialog':'Welcome  Krill', 'location': locations['triad']}],  "What next?", {'Main Menu': {'cmd':'cmd_new_game', 'var':''}, 'Exit':{'cmd':'cmd_exit', 'var':''}})
stg_new_game = Stage('stg_new game', 'new game', [{'speaker':actors['Dmytro_Kaduba'], 'dialog':'Welcome  Krill', 'location': locations['menu']}],  "What next?", {'Main Menu': {'cmd':'cmd_new_game', 'var':''}, 'Exit':{'cmd':'cmd_exit', 'var':''}})
stg_load_game = Stage('stg_load game', 'load game', [{'speaker':actors['Dmytro_Kaduba'], 'dialog':'Welcome  Krill', 'location': locations['menu']}],  "What next?", {'Main Menu': {'cmd':'cmd_new_game', 'var':''}, 'Exit':{'cmd':'cmd_exit', 'var':''}})
stg_exit = Stage('stg_exit', 'Exiting', [{'speaker':actors['Dmytro_Kaduba'], 'dialog':'Welcome  Krill', 'location': locations['menu']}],  "What next?", {'Main Menu': {'cmd':'cmd_new_game', 'var':''}, 'Exit':{'cmd':'cmd_exit', 'var':''}})
stg_lost = Stage('stg_lost', 'You Loose', [{'speaker':actors['Dmytro_Kaduba'], 'dialog':'You lost', 'location': locations['menu']}], "What next?", {'Main Menu': {'cmd':'cmd_new_game', 'var':''}, 'Exit':{'cmd':'cmd_exit', 'var':''}})

stages = { 'stg_main_menu':stg_main_menu, 'stg_act1':stg_act1, 'stg_act1b':stg_act1b, 'stg_new_game':stg_new_game, 'stg_load_game':stg_load_game, 'stg_exit':stg_exit, 'stg_lost':stg_lost, 'stg_stat_choice': stg_stat_choice}

item_names = []
#for item in global_game_items:
	#item_names.append(item.id)

directions = ['north', 'south', 'east', 'west']
action_cmds = ['move', 'take', 'drop']

directions = ['north', 'south', 'east', 'west']
action_cmds = ['move', 'take', 'drop']

keep_words = action_cmds + directions + item_names
