from kivymd.app import MDApp
from kivy.clock import Clock

from db import DataBase
from api import get_countries_data, URL

import pickle

db = DataBase('db.sqlite3')

class MainApp(MDApp):
	
	def __init__(self, **kw):
		super().__init__(**kw)

		self.theme_cls.primary_palette = 'Green'
		self.__update_inteval = 1.00*60* 5 # update every 5 min

	def build(self):
		pass

	def on_start(self) -> None:

		self._confirmed_box = self.root.ids['confirmed_box']
		self._deaths_box    = self.root.ids['deaths_box']
		self._recovered_box = self.root.ids['recovered_box']
		self._new_cases_box = self.root.ids['new_cases_box']

		self._search_box = self.root.ids['tool_bar'].ids['search_box']

		self._country_name = self.root.ids['country_name']

		self.set_vals(0)
		
		# schedule the api call every 15 min
		Clock.schedule_interval(lambda e: self.update_data, 60*10)

	def update_data(self):
		get_countries_data(URL)
		self.set_vals(0)

	def set_vals(self, idx: int) -> None:

		with open('local/_countries_data.pkl', 'rb') as f:
			_data = pickle.load(f)

			__confirmed = _data[idx]['cases']
			__deaths = _data[idx]['deaths']
			__recovered = _data[idx]['recovered']
			__new_cases = _data[idx]['today_cases']

			self._confirmed_box.case_text = self.format_number(__confirmed)
			self._deaths_box.case_text = self.format_number(__deaths)
			self._recovered_box.case_text = self.format_number(__recovered)
			self._new_cases_box.case_text = self.format_number(__new_cases)

	@staticmethod
	def format_number(number: int) -> str:
		if number > 999_999:
			return f'{round(number/1000_000, 2)}M'
		elif number > 999:
			return f'{round(number/1000, 2)}K'
		else:
			return str(number)

	def _search(self) -> None:
		print(self._search_box.text)
		if self._search_box.text == '':
			print('Empty')
			self.set_vals(0)
			self._country_name.text = 'World Wide'
			
		else:
			_country = db.retrive(self._search_box.text)

			if _country:
				self._country_name.text = _country[2]
				self.set_vals(int(_country[0]))


if __name__ == '__main__':
	MainApp().run()
