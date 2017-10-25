import time
from functions import *
from tkinter import *
import json
import random

""" These are the classes which are the structures for different objects in the game """
class Actor():
	#Constructor inits the object with data pulled form DB
	def __init__(self, data):
		#self.speech_color = data['CharID']: 1
		self.fname =  str(data['CharFname']).strip()
		self.lname =  str(data['CharLname']).strip()
		self.name = self.fname + " " + self.lname
		self.id = self.fname + "_" + self.lname
		self.emails = []
		self.stat_points = 20
		self.nickname =  str(data['CharNickname']).strip()
		self.location =  str(data['CharLoc']).strip()
		self.function =  str(data['CharFunc']).strip()
		self.stats = {
			'special': {'str':int(data['CharSTR']), 'per':int(data['CharPER']), 'end':int(data['CharEND']), 'cha':int(data['CharCHA']), 'int':int(data['CharINT']), 'agi':int(data['CharAGI']), 'luc':int(data['CharLUC'])},
			'health': {'curh':0, 'maxh':0},
			'level': {'exp':int(data['CharXP']),'lvl':int(data['CharLevel']),'nxt_lvl':0, 'nxt_exp':0}
		}
		self.wallet = int(data['CharWallet'])
		self.tag = self.id
		#self.tags = {'foreground':data['CharCOL'].strip()}
		self.tags = json.loads(data['CharTags'])
		if self.tags['justify']=='RIGHT': self.tags['justify']=RIGHT
		elif self.tags['justify']=='LEFT': self.tags['justify']=LEFT
		elif self.tags['justify']=='CENTER': self.tags['justify']=CENTER
		else: self.tags['justify']=LEFT
		self.inv = []
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


"""The Stage class allows to navigate through the game"""
class Stage():
	def __init__(self, stage_id, name, narration, question, choices, time = 1):
		self.stage_id = stage_id
		self.name = name
		self.narration = narration #The text to be displayed in this stage (story/dialog)
		#self.choices = choices #The choices availiable at the end of this stage
		self.question = question
		self.choices = {} #The choices availiable at the end of this stage
		self.choicesinput = [] #List of choices to filter out bad input
		for choice, dic in choices.items():
			self.choices[choice.lower()] = dic
			self.choicesinput.append(choice.lower())
		self.time_value = time

class Email:
	def __init__(self, sender, title, text):
		self.sender = sender
		self.title = title
		self.text = text

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
		self.id =  str(data['LocID']).strip()
		self.locname = self.id
		self.name =  str(data['LocName']).strip()
		self.image =  str(data['LocImage']).strip()
		self.description =  str(data['LocID']).strip()
		self.desc = {'short': str(data['LocDescShort']).strip(), 'long1':  str(data['LocDescLong1']).strip(), 'long2':  str(data['LocDescLong2']).strip()}

"""Item class not complete(need to integrate with DB)"""
class Item():
	def __init__(self, data):
		self.id = str(data['ItemTag']).strip()
		self.name = str(data['ItemName']).strip()
		self.type = str(data['ItemType']).strip()
		self.location = str(data['ItemLoc']).strip()
		self.w = float(data['ItemWeight'])
		self.value = int(data['ItemValue'])
		self.buy = int(data['ItemBuyValue'])
		self.sell = int(data['ItemSellValue'])
		self.legal = bool(data['ItemLegal'])
		self.quant = 1
	def inspect():
		#Print out name, description and hints in narration section
		pass
