# -*- coding: utf8 -*-
# v2.1 ( добавлено удаление )
import json
class database:
	def __init__(self,path):
		self.db_path = path
		if self.load() == False:
			self.data = {}
			self.save()
	def save(self):
		try:
			f = open(self.db_path,"w", encoding="utf-8")
			json.dump(self.data,f)
			f.close()
			return True
		except:
			return False
	def load(self):
		try:
			f = open(self.db_path,"r")
			self.data = json.load(f)
			f.close()
			return True
		except:
			return False
	def add(self,key,data):
		if key in self.data:
			return False
		else:
			self.data[key]=data
			self.save()
	def delete(self,key):
		if str(key) in self.data:
			self.data.pop(str(key))
			self.save()
		else:
			return False
