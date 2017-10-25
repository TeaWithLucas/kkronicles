from classes import *

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


		self.functions = {"cmd_new_game":self.cmd_new_game, "cmd_exit":self.cmd_exit, "cmd_back":self.cmd_back, "cmd_change_scene":self.cmd_change_scene, "cmd_lose":self.cmd_lose, "cmd_won":self.cmd_won, "cmd_dialog_choice":self.cmd_dialog_choice, "cmd_make_chems":self.cmd_make_chems, "cmd_create_chems":self.cmd_create_chems, "cmd_caught_police":self.cmd_caught_police, "cmd_start_job":self.cmd_start_job}
		#, "cmd_":self.cmd_, "cmd_":self.cmd_, "cmd_":self.cmd_, "cmd_":self.cmd_, "cmd_":self.cmd_, "cmd_":self.cmd_, "cmd_":self.cmd_, "cmd_":self.cmd_, "cmd_":self.cmd_}


	#Function to update consoles
	def first_run(self):
		self.new_scene()


	#Function to update consoles
	def navigate(self, input_choice):
		print('KEYS> ' + str(self.gui.player.stats['special'].keys()))
		print('inp ' + input_choice[0])
		print(str(self.current_stage))
		functions = self.functions
		if input_choice[0] in self.current_stage.choices:
			cmd = self.current_stage.choices[input_choice[0]]['cmd']
			var = self.current_stage.choices[input_choice[0]]['var']
			if cmd in functions:
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
		remaining_narration = self.current_stage.narration
		for narration in remaining_narration:
			print(self.change_location(narration['location']))
			if self.change_location(narration['location']):
				if narration['speaker'] == self.narrator or narration['speaker'] == self.system_text:
					self.gui.add_txt('narration', narration['dialog'] + '\n\n', narration['speaker'].tag)
				else:
					self.gui.add_txt('narration', narration['speaker'].name + '\n\t"' + narration['dialog'] + '"\n\n', narration['speaker'].tag)
		self.update_choices()

	#Output choices for stage
	def update_choices(self):
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
	def cmd_change_scene(self, args = ""):
		print('cmd_change_scene')
		self.current_stage=self.all_stages[args]
		self.new_scene()
	def cmd_exit(self, args = ""):
		print('cmd_exit')
		quit()
	def cmd_back(self, args = ""):
		print('cmd_back')
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
		print('cmd_start_job')
	def cmd_set_stat(self, stat, value, arg = ""):
		self.gui.player.stats['special'][stat] = value
		self.gui.update_stat_display()
