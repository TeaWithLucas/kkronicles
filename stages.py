from classes import *

"""The Stage Manager allows to easily change stages, take inputs and display all the outputs"""
class Stage_Manager():
	#Inits the stage manager object
	def __init__(self, gui_obj, all_stages, start_stage, narrator, system_text):
		self.all_stages = all_stages
		self.gui_obj = gui_obj
		self.current_stage = start_stage
		self.stages_availiable = []
		self.remaining_narration = self.current_stage.narration
		self.current_location = []
		self.narrator = narrator
		self.system_text = system_text
		self.linebar = '____________________________________________________\n'
		self.function_dict = {
			'void' : self.void,
			'select_stats' : self.select_stats,
			'display_email' : self.display_email,
			'read_email': self.read_email
			}
		self.function_in = ''
		self.stat_list = []
		self.input_in = False
		self.function_arg = ''



	#Will play out the current stage
	def narrate_current_stage(self):
		if self.current_stage.stage_type == 'narrated':
			for narration in self.remaining_narration:
				print(self.change_location(narration['location']))
				if self.change_location(narration['location']):
					if narration['speaker'] == self.narrator:
						self.gui_obj.add_txt('narration', narration['dialog'] + '\n\n', self.system_text.tag)
					else:
						self.gui_obj.add_txt('narration', narration['speaker'].name + ': ' + narration['dialog'] + '\n\n', narration['speaker'].tag)
						#self.gui_obj.add_txt('narration', '_____________________________________________________________________\n\n', 'center_tag', '#FFFACD')
			self.update_choices()
		else:
			self.function_dict[self.current_stage.function](self.function_arg)


	#Output choices for stage
	def update_choices(self):
		for choice in self.current_stage.choices:
			print('c = ' + choice)
			self.gui_obj.add_txt('choice', '\n[' + choice.upper() + ']    \n', self.narrator.tag)


	#Fetches user input
	def take_nar_input(self, input):
		if input == 'exit':
			quit()
		else:
			self.current_stage = self.select_stage(self.current_stage.choices[input])
			self.get_narration()

	def take_func_input(self, input):
		print('Input taken')
		self.function_in = input
		self.input_in = True


	#Select the right stage after input
	def select_stage(self, text):
		for stage in self.all_stages:
			if text == stage.stage_id:
				return stage


	#Gets the remaining_narration
	def get_narration(self):
		self.remaining_narration = self.current_stage.narration

	#Changes the location of the player and displays appropriate narrations
	def change_location(self, new_location):
		if self.current_location != new_location:
			img_loc = './assets/' + new_location.image
			print('img location: ' + img_loc)
			self.gui_obj.change_image('loc_img', img_loc)
			self.gui_obj.update_label('loc_desc', new_location.name)
			if new_location.id != 'menu':
				self.gui_obj.add_txt('narration', self.linebar + new_location.desc['long1'] + '\n' + self.linebar, self.narrator.tag)
			#self.gui_obj.cur_loc = new_location.name
			self.current_location = new_location
			return False
		else:
			return True



	def select_stats(self, arg):
		for stat in self.gui_obj.player.stats['special']:
			if self.gui_obj.player.availiable_stat_points > 0:
				self.gui_obj.add_txt('narration', '[APPLICATION FORM]', self.narrator.tag)
				self.gui_obj.add_txt('narration', '\n\nYou have ' + str(self.gui_obj.player.availiable_stat_points) + ' points left', self.narrator.tag)
				self.gui_obj.add_txt('narration', '\n\nHow much ' + stat.upper() + '?', self.narrator.tag)
				while not self.input_in:
					print('Waiting')
					self.gui_obj.main.update()

				if int(self.function_in) <= self.gui_obj.player.availiable_stat_points:
					self.gui_obj.player.stats['special'][stat] = self.function_in
					self.gui_obj.player.availiable_stat_points -= int(self.function_in)
					self.function_in = ''
					self.gui_obj.clear_middle()
					self.input_in = False
					self.gui_obj.update_stat_display()
				else:
					self.gui_obj.clear_middle()
					self.gui_obj.add_txt('narration', 'Not enough points', self.narrator.tag)
					break

			else:
				self.gui_obj.clear_middle()
				self.gui_obj.add_txt('narration', 'You have no more points left!', self.narrator.tag)
				break

		self.next_stage()

	def display_email(self, arg):
		self.gui_obj.clear_middle()
		self.gui_obj.add_txt('narration', 'You open your emails.\n\n', self.narrator.tag)
		if self.gui_obj.player.emails:
			self.gui_obj.add_txt('narration', 'You have ' + str(len(self.gui_obj.player.emails)) + ' emails to read:\n\n', self.system_text.tag)
			for email in self.gui_obj.player.emails:
				text = 'from ' + email.sender
				self.gui_obj.add_txt('narration', '       >> '+ text + '\n\n', self.system_text.tag)
				self.current_stage.choices.update({'open ' + text: 'read_email'})

			self.update_choices()
			while not self.input_in:
				print('Waiting')
				self.gui_obj.main.update()
			self.input_in = False
			email = ''
			choice = self.function_in
			list_words = choice.split()
			for e in self.gui_obj.player.emails:
				if e.sender == list_words[2]:
					email = e
			self.function_arg = email
			self.current_stage = self.select_stage(self.current_stage.choices[self.function_in])
			print(self.current_stage.name)
			self.narrate_current_stage()


		else:
			self.gui_obj.clear_middle()
			self.gui_obj.add_txt('narration', 'You have 0 emails to read.\n\n', self.system_text.tag)



	def read_email(self, email):
		print('Executed read_email')
		print(str(email))
		self.gui_obj.clear_middle()
		self.gui_obj.add_txt('narration', email.title + '\n\n', self.narrator.tag)
		self.gui_obj.add_txt('narration', email.text + '\n\n', self.system_text.tag)
		self.gui_obj.add_txt('narration', email.sender.upper() + '\n', self.system_text.tag)
		self.update_choices()
		while not self.input_in:
			print('Waiting')
			self.gui_obj.main.update()
		self.input_in = False
		print('CLOSE')
		self.current_stage = self.select_stage(self.current_stage.choices[self.function_in])
		print(self.current_stage.name)
		self.narrate_current_stage()



	def next_stage(self):
		self.current_stage = self.select_stage(self.current_stage.next_stg)
		print(self.current_stage)
		self.get_narration()
		self.narrate_current_stage()


	def void(self):
		pass


	#def load_loc_description(self):
	#	location_description = self.current_stage.location.description
	#	if not (location_description == ''):
	#		self.current_stage.narration.insert(0, {'speaker':self.narrator, 'dialog':location_description})
