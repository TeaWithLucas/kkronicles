from classes import *
from data import *
import random
from functions import draw_ascii

"""The Stage Manager allows to easily change stages, take inputs and display all the outputs"""
class Stage_Manager():
	#Inits the stage manager object
	def __init__(self, gui, all_stages, start_stage, narrator, system_text):
		self.all_stages = all_stages
		self.gui = gui
		self.current_stage = start_stage
		self.stages_availiable = []
		self.remaining_narration = self.current_stage.narration
		self.current_location = []
		self.narrator = narrator
		self.system_text = system_text
		self.linebar = '____________________________________________________\n'
		self.player_emails = self.gui.player.emails
		self.prev_choices = ''
		self.prev_list_choices = []
		self.email_disp = False
		self.email_read = False
		self.job_offered = False
		self.job_completed = False
		self.anon_email_read = False
		self.triad_email_read = False
		self.triad_rejected = False
		self.labs_first = True
		self.functions = {"cmd_combat": self.cmd_combat,"cmd_get_money": self.cmd_get_money, "cmd_restart": self.cmd_restart,"cmd_take_risk": self.cmd_take_risk, "cmd_loot": self.cmd_loot, "cmd_buy_item": self.cmd_buy_item, "cmd_display_items": self.cmd_display_items, "cmd_rnd_stats": self.cmd_rnd_stats, "cmd_move_location": self.cmd_move_location, "cmd_sell_item": self.cmd_sell_item, "cmd_cook_drug": self.cmd_cook_drug, "cmd_cook_menu": self.cmd_cook_menu,"cmd_change_stage": self.cmd_change_stage, "cmd_sell_online": self.cmd_sell_online, "cmd_open_tor": self.cmd_open_tor, "cmd_read_email": self.cmd_read_email,"cmd_display_emails": self.cmd_display_emails,"cmd_new_game":self.cmd_new_game, "cmd_exit":self.cmd_exit, "cmd_choose":self.cmd_choose, "cmd_change_scene":self.cmd_change_scene, "cmd_lose":self.cmd_lose, "cmd_won":self.cmd_won, "cmd_dialog_choice":self.cmd_dialog_choice, "cmd_make_chems":self.cmd_make_chems, "cmd_create_chems":self.cmd_create_chems, "cmd_caught_police":self.cmd_caught_police, "cmd_start_job":self.cmd_start_job}


	#Function to update consoles
	def first_run(self):
		self.new_scene()


	#Function to update consoles
	def navigate(self, input_choice):
		if self.gui.player.wallet > 500000000:
			self.cmd_change_scene('stg_win_game')
		else:
			print('KEYS> ' + str(self.gui.player.stats['special'].keys()))
			print('inp ' + input_choice[0])
			print(str(self.current_stage))
			functions = self.functions
			whole_input = ''
			first = True
			for word in input_choice:
				if first:
					whole_input = word
					first = False
				else:
					whole_input +=  ' ' + word
			if whole_input in self.current_stage.choices:
				cmd = self.current_stage.choices[whole_input]['cmd']
				var = self.current_stage.choices[whole_input]['var']
				if cmd in functions:
					self.current_stage.revert_choices()
					functions[cmd](var)

			elif input_choice[0] in self.gui.player.stats['special'].keys() and self.current_stage == self.all_stages['stg_stat_choice']:
				print('Doing stats')
				self.cmd_set_stat(input_choice[0],input_choice[1])

			else:
				self.update_choices()



	def new_scene(self):
		self.gui.clear_middle() #Clear consoles
		self.gui.refresh() #Update secondary consoles
		self.gui.set_title(self.current_stage.name) #Set correct window title
		self.narrate_current_stage() #Start narration of the stage

	#Will play out the current stage
	def narrate_current_stage(self):
		if self.current_stage == self.all_stages['stg_main_menu']:
			self.cmd_main()
		else:
			remaining_narration = self.current_stage.narration
			for narration in remaining_narration:
				print(self.change_location(locations[narration['location']]))
				if self.change_location(locations[narration['location']]):
					speaker = actors[narration['speaker']]
					if speaker== self.narrator or speaker == self.system_text:
						self.gui.add_txt('narration', narration['dialog'] + '\n\n',  speaker.tag)
					else:
						self.gui.add_txt('narration', speaker.name + '\n\t"' + narration['dialog'] + '"\n\n', speaker.tag)
		self.update_choices()


	#Output choices for stage
	def update_choices(self):
		self.gui.clear_choices()
		self.gui.add_txt('choice', "\t" + self.current_stage.question + "\n", self.system_text.tag)
		for choice in self.current_stage.choicesinput:
			print('c = ' + choice)
			self.gui.add_txt('choice', '\n[' + choice.upper() + ']    \n', self.narrator.tag)



	#Fetches user input
	#def take_input(self, input):
		#if input == 'exit':
		#	quit()
		#else:
		#	self.current_stage = self.select_stage(self.current_stage.choices[input])
		#	self.get_narration()

	#Select the right stage after input
	def select_stage(self, text):
		for stage in self.all_stages:
			if text == stage.stage_id:
				return stage

	#Changes the location of the player and displays appropriate narrations
	def change_location(self, new_location):
		if self.current_location != new_location:
			img_loc = './assets/' + new_location.image
			print('img location: ' + img_loc)
			self.gui.change_image('loc_img', img_loc)
			self.gui.update_label('loc_desc', new_location.name)
			if new_location.id != 'menu':
				self.gui.add_txt('narration', self.linebar + '\n' + new_location.desc['long1'] + '\n' + self.linebar + '\n', self.narrator.tag)
			#self.gui.cur_loc = new_location.name
			self.current_location = new_location
			return False
		else:
			return True

	#game logic section

	def cmd_new_game(self, args = ""):
		print('cmd_new_game')
		#insert code to reset game here
		self.current_stage=stages['stg_main_menu']
		self.new_scene()
	def cmd_change_stage(self, args = ""):
		self.cmd_change_scene(args)
	def cmd_change_scene(self, args = ""):
		print('cmd_change_scene')
		self.current_stage=self.all_stages[args]
		if self.email_disp:
			self.current_stage.choices = self.prev_choices
			self.current_stage.choicesinput = self.prev_list_choices
		self.new_scene()
	def cmd_exit(self, args = ""):
		print('cmd_exit')
		quit()
	def cmd_choose(self, args = ""):
		print('cmd_choose')
		options = args.split(" ")
		if options[0] == "faction":
			if options[1] == "taffia":
				self.gui.player.faction = "taffia"
			elif options[1] == "triad":
				self.gui.player.faction = "triad"
		elif options[0] == "job":
			self.job_offered = True
			if options[1] == "refuse":
				self.gui.player.faction = "indie"
		self.cmd_change_stage(options[2])

	def cmd_lose(self, args = ""):
		print('cmd_lose')
	def cmd_won(self, args = ""):
		print('cmd_won')
	def cmd_dialog_choice(self, args = ""):
		print('cmd_dialog_choice')
	def cmd_make_chems(self, args = ""):
		print('cmd_make_chems')
	def cmd_create_chems(self, args = ""):
		print('cmd_create_chems')
	def cmd_caught_police(self, args = ""):
		print('cmd_caught_police')
	def cmd_start_job(self, args = ""):
		if self.job_completed:
			self.gui.add_txt('narration', 'No jobs currently availiable\n\n', self.narrator.tag)
			self.current_stage.choicesinput = []
			self.current_stage.choicesinput.append('close')
			if args == 'taff':
				self.current_stage.choices.update({'close': {'cmd':'cmd_change_scene', 'var': "stg_at_taff"}})
			elif args == 'triad':
				self.current_stage.choices.update({'close': {'cmd':'cmd_change_scene', 'var': "stg_at_triad"}})
			self.update_choices()

		else:
			if args == 'taff':
				self.cmd_change_scene('stg_job_offer_taffia')
			elif args == 'triad':
				self.cmd_change_scene('stg_job_offer_triad')

	def cmd_rnd_stats(self, arg = ""):
		self.gui.player.stats['special'] = {'str':6, 'per':6, 'end':6, 'cha':6, 'int':6, 'agi':6, 'luc':6}
		self.gui.player.stat_points = 0
		self.gui.player.calc_stats()
		self.cmd_change_stage("stg_stat_choice")
	def cmd_set_stat(self, stat, value, arg = ""):
		if self.gui.player.stat_points - int(value) > 0:
			self.gui.player.stat_points -= int(value) - self.gui.player.stats['special'][stat]
			self.gui.player.stats['special'][stat] = int(value)
			self.gui.player.calc_stats()
			self.gui.update_stat_display()
		else:
			self.gui.add_txt('narration', '[NOT ENOUGH POINTS]', self.narrator.tag)


	def cmd_display_emails(self, args = ""):
			#self.email_read = True
			self.gui.clear_middle()
			self.gui.add_txt('narration', 'You open your email\n\n', self.narrator.tag)
			self.gui.add_txt('narration', 'You have ' + str(len(self.gui.player.emails)) + ' emails:\n\n', self.system_text.tag)
			choices_to_add = []
			for email in self.gui.player.emails:
				text = '\t>> From ' + email.sender + '\n'
				choices_to_add.append(email.sender)
				self.gui.add_txt('narration', text, self.system_text.tag)

			self.current_stage.choicesinput = []
			for c in choices_to_add:
				self.current_stage.choicesinput.append('open from ' + c)
				self.current_stage.choices.update({'open from ' + c : {'cmd':'cmd_read_email', 'var': c}})
			self.current_stage.choicesinput.append('close')
			self.current_stage.choices.update({'close': {'cmd':'cmd_open_tor', 'var': ""}})
			self.update_choices()

	def cmd_read_email(self, args = ""):
		if args == 'z':
			self.anon_email_read = True
		if args == 'white tiger':
			self.triad_email_read = True
		#self.email_read = True
		email_to_read = ''
		for e in self.player_emails:
			if e.sender == args:
				email_to_read = e
		self.gui.clear_middle()
		self.gui.add_txt('narration', email_to_read.title.upper() +'\n\n', self.narrator.tag)
		self.gui.add_txt('narration', email_to_read.text +'\n', self.system_text.tag)
		self.gui.add_txt('narration', email_to_read.sender.upper() +'\n', self.system_text.tag)
		self.current_stage.choicesinput = []
		self.current_stage.choicesinput.append('close')
		self.current_stage.choices.update({'close' : {'cmd':'cmd_display_emails', 'var': ''}})
		self.update_choices()

	def cmd_open_tor(self, args = ""):
		#self.email_disp = True
		#if not(self.email_read):
			#self.prev_choices = self.current_stage.choices
			#self.prev_list_choices = self.current_stage.choicesinput
			#self.email_read = False
		print('Opened TOR')
		self.gui.clear_middle()
		self.gui.add_txt('narration', 'You open Tor Browser\n\n', self.narrator.tag)
		self.gui.add_txt('narration', 'BREAKIN NEWS\n\n', self.narrator.tag)
		self.gui.add_txt('narration', '[HACKER HIJACKS]\n', self.system_text.tag)
		self.gui.add_txt('narration', 'A new widespread ransomware attack is spreading like wildfire around Europe and has already affected over 200 major organisations, primarily in Russia, Ukraine, Turkey and Germany, in the past few \n\n', self.system_text.tag)
		self.gui.add_txt('narration', '[BAD RABBIT]\n', self.system_text.tag)
		self.gui.add_txt('narration', "When yesterday I was reporting about the sudden outbreak of another global ransomware attack 'Bad Rabbit,' I thought what could be worse than this? Then late last night I got my answer with a notification\n\n", self.system_text.tag)
		self.gui.add_txt('narration', '[DUHK ATTACK]\n', self.system_text.tag)
		self.gui.add_txt('narration', "DUHK — Don't Use Hard-coded Keys — is a new 'non-trivial' cryptographic implementation vulnerability that could allow attackers to recover encryption keys that secure VPN connections and web browsing\n\n", self.system_text.tag)

		self.current_stage.choicesinput = []
		self.current_stage.choicesinput.append('sell online')
		self.current_stage.choices.update({'sell online' : {'cmd':'cmd_sell_online', 'var': ''}})
		self.current_stage.choicesinput.append('email')
		self.current_stage.choices.update({'email' : {'cmd':'cmd_display_emails', 'var': ''}})
		self.current_stage.choicesinput.append('close')
		self.current_stage.choices.update({'close' : {'cmd':'cmd_change_scene', 'var': self.current_stage.id}})

		self.update_choices()


	def cmd_sell_online(self, args = ""):
		print('Sell Online')
		self.email_read = True
		items_to_sell = []
		for item in self.gui.player.inv:
			if item.type == 'Drug':
				items_to_sell.append(item)

		self.gui.clear_middle()
		self.gui.add_txt('narration', 'THE SILK ROAD\n\n', self.narrator.tag)
		self.gui.add_txt('narration', 'Now choose what you want to sell...\n\n', self.system_text.tag)

		self.current_stage.choicesinput = []
		found = False
		if items_to_sell:
			self.current_stage.choicesinput.append('sell all drugs')
			self.current_stage.choices.update({'sell all drugs' : {'cmd':'cmd_sell_item', 'var': ''}})

		self.current_stage.choicesinput.append('close')
		self.current_stage.choices.update({'close' : {'cmd':'cmd_open_tor', 'var': ''}})
		self.update_choices()



	def cmd_sell_item(self, args = ""):
		self.gui.player.police_alert += 2
		#self.email_read = True
		list_items = self.gui.player.inv
		for item in list_items:
			if item.type == 'Drug' :
				self.gui.player.inv.remove(item)
				self.gui.player.wallet += item.sell
		self.gui.update_inv_display()
		self.gui.update_wallet()
		items_to_sell = []
		for item in self.gui.player.inv:
			if item.type == 'Drug':
				items_to_sell.append(item)

		self.cmd_sell_online()

	def cmd_cook_menu(self, arg = ""):
		#self.email_disp = True
		#if not(self.email_read):
			#self.prev_choices = self.current_stage.choices
			#self.prev_list_choices = self.current_stage.choicesinput
			#self.email_read = False
		self.gui.clear_middle()
		self.gui.add_txt('narration', 'Recepie Book\n\n', self.narrator.tag)
		self.gui.add_txt('narration', 'Here you can cook your very own drugs! Have fun...\n\n', self.system_text.tag)
		possibilities = self.gui.recipe_engine.check_for_possibilities(self.gui.player.inv)
		self.gui.add_txt('narration', 'With your items you can make:\n\n', self.system_text.tag)
		self.current_stage.choicesinput = []
		for c in possibilities:
			drug_name = ''
			drug_id = c.output
			for item in items.values():
				print(item.id + ' - ' + c.output)
				if c.output == item.id:
					drug_name = item.name

			self.gui.add_txt('narration', '\t\t' + drug_name + '\n\n', self.system_text.tag)

			self.current_stage.choicesinput.append('cook ' + drug_name)
			self.current_stage.choices.update({'cook ' + drug_name.lower() : {'cmd':'cmd_cook_drug', 'var': drug_id}})

		self.current_stage.choicesinput.append('close')
		self.current_stage.choices.update({'close' : {'cmd':'cmd_change_scene', 'var': self.current_stage.id}})
		self.update_choices()

	def cmd_cook_drug(self, drug_id):
		self.email_read = True
		print('Cooking...')
		drug_item = ''
		for item in items.values():
			if item.id == drug_id:
				drug_item = item
		self.gui.player.take(drug_item)
		remove_list = []
		all_game_rec = self.gui.recipe_engine.all_recepies
		for rec in all_game_rec.values():
			if rec.output == drug_id:
				remove_list += rec.input.values()
		print(remove_list)
		for item in remove_list:
			for i in items.values():
				if i.id == item:
					self.gui.player.drop(i)
		self.gui.update_inv_display()
		self.cmd_cook_menu()


	def cmd_move_location(self, args = ""):
		print('We moved')
		self.gui.clear_choices()
		self.current_stage.choicesinput = []
		if self.gui.player.faction == 'taffia':
			#taf
			self.current_stage.choicesinput.append('go taff')
			self.current_stage.choices.update({'go taff' : {'cmd':'cmd_change_scene', 'var': 'stg_at_taff'}})


		if self.gui.player.faction == 'triad':
			#triad
			self.current_stage.choicesinput.append('go triad')
			self.current_stage.choices.update({'go triad' : {'cmd':'cmd_change_scene', 'var': 'stg_at_triad'}})
		elif self.triad_email_read and self.triad_rejected == False:
			self.triad_rejected = True
			self.current_stage.choicesinput.append('go triad')
			self.current_stage.choices.update({'go triad' : {'cmd':'cmd_change_scene', 'var': 'stg_the_triad'}})


		if self.anon_email_read:
			self.current_stage.choicesinput.append('go park')
			self.current_stage.choices.update({'go park' : {'cmd':'cmd_change_scene', 'var': 'stg_park'}})



		if self.labs_first:
			self.labs_first = False
			self.current_stage.choicesinput.append('go labs')
			self.current_stage.choices.update({'go labs' : {'cmd':'cmd_change_scene', 'var': 'stg_labs_first'}})
		else:
			self.current_stage.choicesinput.append('go labs')
			self.current_stage.choices.update({'go labs' : {'cmd':'cmd_change_scene', 'var': 'stg_labs'}})
		#always libarary, uni
		self.current_stage.choicesinput.append('go library')
		self.current_stage.choices.update({'go library' : {'cmd':'cmd_change_scene', 'var': 'stg_at_library'}})
		self.current_stage.choicesinput.append('go teach')
		self.current_stage.choices.update({'go teach' : {'cmd':'cmd_change_scene', 'var': 'stg_job_lecture'}})

		self.update_choices()

	def cmd_display_items(self, arg = ""):
		if arg == 'taff':
			self.gui.clear_middle()
			self.gui.add_txt('narration', "You approch Claws\n", self.narrator.tag)
			self.gui.add_txt('narration', actors['James_Wills'].name + "\n\t'ight? 'eres what we got", actors['James_Wills'].tag)
			items_on_sale = []
			for item in items.values():
				if item.type == 'Drug':
					items_on_sale.append(item)
			self.current_stage.choicesinput = []
			for item in items_on_sale:
				self.gui.add_txt('narration', '\n\t>' + item.name +  ' -- ' + str(item.value*0.8), self.system_text.tag)
				self.current_stage.choicesinput.append('buy ' + item.name)
				self.current_stage.choices.update({'buy ' + item.name.lower() : {'cmd':'cmd_buy_item', 'var': item.id + ' taff'}})
			self.current_stage.choicesinput.append('close')
			self.current_stage.choices.update({'close': {'cmd':'cmd_change_scene', 'var': 'stg_at_taff'}})
			self.update_choices()
		elif arg == 'triad':
			self.gui.clear_middle()
			self.gui.add_txt('narration', "You approch Snake\n", self.narrator.tag)
			self.gui.add_txt('narration', actors['She_Ni'].name + "\n\t'Hello b i ch? (??)", actors['She_Ni'].tag)
			items_on_sale = []
			for item in items.values():
				if item.type == 'Drug':
					items_on_sale.append(item)
			self.current_stage.choicesinput = []
			for item in items_on_sale:
				self.gui.add_txt('narration', '\n\t>' + item.name +  ' -- ' + str(item.value*0.8), self.system_text.tag)
				self.current_stage.choicesinput.append('buy ' + item.name)
				self.current_stage.choices.update({'buy ' + item.name.lower() : {'cmd':'cmd_buy_item', 'var': item.id + ' triad'}})
			self.current_stage.choicesinput.append('close')
			self.current_stage.choices.update({'close': {'cmd':'cmd_change_scene', 'var': 'stg_at_triad'}})
			self.update_choices()

	def cmd_buy_item(self, arg = ""):
		self.gui.player.police_alert += 2
		arg_list = arg.split()
		item_bought = ''
		for i in items.values():
			if i.id == arg_list[0]:
				item_bought = i
		for n in range(0,5):
			self.gui.player.inv.append(item_bought)
		self.gui.update_inv_display()
		self.gui.player.wallet -= item_bought.buy * 5
		self.gui.update_wallet()
		self.cmd_display_items(arg_list[1])

	def cmd_take_risk(self, arg = ""):
		if random.randrange(0, self.gui.player.police_alert) > 20:
			#Get caught
			if arg == 'park':
				self.cmd_change_scene('stg_caught_park')
			elif arg == 'labs':
				self.cmd_change_scene('stg_caught_labs')
		else:
			#take loot
			if arg == 'park':
				self.cmd_change_scene('stg_leave_park')
			elif arg == 'labs':
				self.cmd_change_scene('stg_labs_success')

	def cmd_loot(self, arg = ""):
		self.gui.player.police_alert += 3
		for item in items.values():
			if item.type == 'Ingredient':
				self.gui.player.inv.append(item)
		self.cmd_change_scene('stg_home')

	def cmd_get_money(self, arg = ""):
		self.gui.player.wallet += 50 * 2300000
		self.cmd_change_scene('stg_home')

	def cmd_restart(self, arg = ""):
		data.reload_data()

#{"Continue": {"cmd":"cmd_combat", "var":"stg_job_taffia_win_strength stg_job_taffia_win_perception stg_job_taffia_escape stg_job_taffia_die"}}

#{"Continue": {"cmd":"cmd_combat", "var":"stg_job_triad_win_strength stg_job_triad_win_perception stg_job_triad_escape stg_job_triad_die"}}
	def cmd_combat(self, args = ""):
		list_of_options = args.split()
		stre = self.gui.player.stat_check('str')
		per = self.gui.player.stat_check('per')
		agi = self.gui.player.stat_check('agi')

		if stre > 6 or per > 6:
			if stre > per:
				self.cmd_change_scene(list_of_options[0])
			else:
				self.cmd_change_scene(list_of_options[1])

		elif agi > 6:
			self.cmd_change_scene(list_of_options[2])

		else:
			self.cmd_change_scene(list_of_options[3])

	def cmd_main(self, args = ""):
		output = draw_ascii('./assets/welcome.txt')
		self.gui.add_txt('narration', output, self.system_text.tag)
