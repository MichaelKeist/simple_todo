#A fun little project that makes a simple todo list.
#Will have a way to submit todo items with task and date
#Will have interactive calendar to find due dates easily
#Will be able to get a list of all todo items sorted in different ways

#Items cannot contain the '~' symbol (used as a separator in writing to file)

import os
from datetime import datetime
import pandas

#definition of a single todo element
class todo_item:
	def __init__(self, name, due_date, note = ""):
		self.__name = name
		self.__due_date = due_date
		self.__note = note
		pass

	def __str__(self):
		return self.__name + " due: " + self.__due_date

	def get_date(self):
		return self.__due_date

	def get_name(self):
		return self.__name

	def set_date(self, new_date):
		self.__due_date = new_date
		pass

	def set_name(self, new_name):
		self.__name = new_name

	def set_note(self, new_note):
		self.__note = new_note

	def get_note(self):
		return self.__note

#definition of a list of todo elements
class todo_list:
	def __init__(self, todo_items = []):
		self.__todo_items = todo_items
		self.__n = 0

	def __str__(self):
		output_str = ""
		count = 1
		for item in self.__todo_items:
			output_str += str(count) + ": " + item.get_name() + " due: "
			output_str += item.get_date() + "\n"
			count += 1
		return output_str

	def write_to_file(self, location = os.path.expanduser('~') + "/.config/.my_todo"):
		output_str = ""
		save_file = open(location, "w")
		for item in self.__todo_items:
			output_str += item.get_name() + "~"
			output_str += item.get_date() + "~"
			output_str += item.get_note() + "\n"
		save_file.write(output_str)
		save_file.close()

	def add_item(self, todo_item):
		self.__todo_items.append(todo_item)

	def __len__(self):
		return len(self.__todo_items)

	def __getitem__(self, key):
		return self.__todo_items[key]

	def __iter__(self):
		return self

	def __next__(self):
		if self.__n <= (len(self) - 1):
			result = self[self.__n]
			self.__n += 1
			return result
		else:
			self.__n = 0
			raise StopIteration

	#def due_sort(self): #outputs a todo list sorted by associated dates
		#output_todos = todo_list([])
		#name_list = [self[x].get_name() for x in range(0, len(self))]
		#date_list = [self[x].get_date() for x in range(0, len(self))]
		#date_series = pandas.Series(date_list)
		#date_series = pandas.to_datetime(date_series, infer_datetime_format = True)
		#date_series = date_series.sort_values()
		#for item in date_series.items():
		#	index = item[0]
		#	date = str(item[1])[5:8] + str(item[1])[8:10] + "-" + str(item[1])[0:4]
		#	current_item = todo_item(name_list[index], date)
		#	output_todos.add_item(current_item)
		#return output_todos

	#calculate number of days since 01-01-0000, and sort items by that score
	def due_sort(self): #the scores for each date are not exactly the number of days since 01-01-0000 but eh
		month_lengths = [31,28,31,30,31,30,31,31,30,31,30,31]
		output_todos = todo_list([])
		index_list = [x for x in range(0,len(self))]
		date_weights = []
		item_list = [item for item in self]
		for item in item_list:
			current_weight = 0
			split_date = item.get_date().split("-")
			current_weight += (int(split_date[2]) - 1) * 365 + int(split_date[1])
			for i in range(0,int(split_date[0]) - 1):
				current_weight += month_lengths[i]
			date_weights.append(current_weight)
		ordered_index = [x for _, x in sorted(zip(date_weights, index_list))] #sorting a list of indices by the date scores
		for index in ordered_index:
			output_todos.add_item(self[index])
		return output_todos

	def remove(self, index):
		self.__todo_items.__delitem__(index)
		
def read_todo_list(location = os.path.expanduser('~') + "/.config/.my_todo"): #defines default path to search for existing todo list
	file = open(location, "r")
	output_todos = todo_list()
	for i in file:
		data = i.strip().split("~")
		note = "" if len(data) == 2 else data[2]
		output_todos.add_item(todo_item(data[0], data[1], note))
	file.close()
	return output_todos


#x = read_todo_list()
#for i in range(10,10000):
#	name_str = "test" + str(i)
#	date_str = "01-01-19" + str(i)
#	y = todo_item(name_str, date_str)
#	x.add_item(y)
#y = x.due_sort()
#y.write_to_file()
#y.add_item(z)
#print(y.due_sort())