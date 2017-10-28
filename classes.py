import time
from functions import *
from tkinter import *
import random
import json

""" These are the classes which are the structures for different objects in the game """
class Actor():
	#Constructor inits the object with data pulled form DB
	def __init__(self, data):

		#self.speech_color = data['actor_ID']: 1
		self.fname =  str(data['actor_Fname']).strip()
		self.lname =  str(data['actor_Lname']).strip()
		self.nickname =  str(data['actor_Nickname']).strip()
		self.id =  str(data['actor_StrID']).strip()

		nametype = int(data['actor_NickUse'])
		name = ""
		if nametype == 0: name = self.nickname
		elif nametype == 1: name = self.fname + " " + self.lname
		elif nametype == 2: name = self.fname

		self.name = name
		self.emails = []
		self.stat_points = 45
		
		self.location =  str(data['actor_Loc']).strip()
		self.function =  str(data['actor_Func']).strip()
		self.stats = {
			'special': {'str':int(data['actor_STR']), 'per':int(data['actor_PER']), 'end':int(data['actor_END']), 'cha':int(data['actor_CHA']), 'int':int(data['actor_INT']), 'agi':int(data['actor_AGI']), 'luc':int(data['actor_LUC'])},
			'health': {'curh':0, 'maxh':0},
			'level': {'exp':int(data['actor_XP']),'lvl':int(data['actor_Level']),'nxt_lvl':0, 'nxt_exp':0}
		}
		self.wallet = int(data['actor_Wallet'])
		self.tag = self.id
		#self.tags = {'foreground':data['actor_COL'].strip()}
		self.tags = json.loads(data['actor_Tags'])
		if self.tags['justify']=='RIGHT': self.tags['justify']=RIGHT
		elif self.tags['justify']=='LEFT': self.tags['justify']=LEFT
		elif self.tags['justify']=='CENTER': self.tags['justify']=CENTER
		else: self.tags['justify']=LEFT
		self.inv = []
		self.police_alert = 1
		self.faction = 'indie'
		self.calc_stats()


	#calculates the currect stats of the actor
	def calc_stats(self):
		cur_maxh = self.stats['health']['maxh']
		cur_curh = self.stats['health']['curh']
		new_maxh = self.stats['level']['lvl'] * 8 + self.stats['special']['end'] * 8
		new_curh = cur_curh + (new_maxh - cur_maxh)
		self.stats['health'] = {'maxh': new_maxh, 'curh': new_curh}

	def add_email(self, email):
		self.emails.append(email)

	def take(self, item):
		self.inv.append(item)

	def drop(self, item):
		self.inv.remove(item)

	def stat_check(self, stat_to_check):
		stat_value = self.stats['special'][stat_to_check]
		luc_stat = self.stats['special']['luc']
		stat_modifier = (random.randrange(0,luc_stat) - 1) + random.randrange(-5,5)
		stat_return = stat_value + stat_modifier
		return stat_return

class Recipe():

	def __init__(self, data):
			self.id = str(data['rec_id']).strip()
			self.name = str(data['rec_name']).strip()
			self.input = json.loads(data['rec_input'])
			self.output = str(data['rec_output']).strip()
			self.method = str(data['rec_method']).strip()


class Recipe_Manager():

		def __init__(self, all_recepies):
			self.all_recepies = all_recepies

		def check_for_possibilities(self,inventory):
			possible_recepy_list = []
			inventory_ids = []
			for item in inventory:
				inventory_ids.append(item.id)
			for recepy in self.all_recepies.values():
				current_rec_input = recepy.input.values()
				print(current_rec_input in inventory)
				print(current_rec_input)
				if all(x in inventory_ids for x in current_rec_input):
					print('MATCH')
					possible_recepy_list.append(recepy)

			return possible_recepy_list




"""The Stage class allows to navigate through the game"""
class Stage():
	def __init__(self, data):
		self.id = str(data['stages_id']).strip()
		self.name = str(data['stages_name']).strip()
		self.narration = [] #The text to be displayed in this stage (story/dialog)
		self.question = data['stages_questions']
		#self.question = str("needs to be put on db").strip()
		self.cmd = json.loads(data['stages_choices'])
		self.choices = {}
		choices = json.loads(data['stages_choices']) #The choices availiable at the end of this stage
		self.choicesinput = [] #List of choices to filter  out bad input
		for choice, dic in choices.items():
			self.choices[str(choice).lower().strip()] = dic
			self.choicesinput.append(str(choice).lower().strip())
		self.choices_orig = {}
		choices = json.loads(data['stages_choices']) #The choices availiable at the end of this stage
		self.choicesinput_orig = [] #List of choices to filter  out bad input
		for choice, dic in choices.items():
			self.choices_orig[str(choice).lower().strip()] = dic
			self.choicesinput_orig.append(str(choice).lower().strip())

	def narration_add(self, data):
		for row in data:
			tempdict = {'speaker':str(row['narr_speaker']).strip(), 'location':str(row['narr_location']).strip(), 'order':int(row['narr_order']), 'dialog':str(row['narr_dialog'])}
			self.narration.append(tempdict)
	def revert_choices(self):
		self.choices = {}
		self.choicesinput = []
		choices = self.choices_orig
		for choice, dic in choices.items():
			self.choices[choice] = dic
			self.choicesinput.append(choice)

"""The location class allows to navigate through the game map and describe locations in the narration """

class Location():
	#def __init__(self, locname, name, image = "", desc = ""):
		#self.id = locname
		#self.locname = locname
		#self.name = name
		#self.image = image
		#self.description = desc

	#Constructor pulls location data from DB
	def __init__(self, data):
		self.id =  str(data['loc_ID']).strip()
		self.locname = self.id
		self.name =  str(data['loc_Name']).strip()
		self.image =  str(data['loc_Image']).strip()
		self.description =  str(data['loc_ID']).strip()
		self.desc = {'short': str(data['loc_DescShort']).strip(), 'long1':  str(data['loc_DescLong1']).strip(), 'long2':  str(data['loc_DescLong2']).strip()}

"""Item class not complete(need to integrate with DB)"""
class Item():
	def __init__(self, data):
		self.id = str(data['item_Tag']).strip()
		self.name = str(data['item_Name']).strip()
		self.type = str(data['item_Type']).strip()
		self.location = str(data['item_Loc']).strip()
		self.w = float(data['item_Weight'])
		self.value = int(data['item_Value']) * 230000
		self.buy = int(data['item_BuyValue']) * 230000
		self.sell = int(data['item_SellValue']) * 230000
		self.legal = bool(data['item_Legal'])
		self.quant = 1
	def inspect():
		#Print out name, description and hints in narration section
		pass

class Email:
	def __init__(self, sender, title, text):
		self.sender = sender
		self.title = title
		self.text = text
