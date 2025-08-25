import pymongo
import os
from Config import config
from dotenv import load_dotenv, find_dotenv
import dns.resolver
from colorama import Fore

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

#load dotenv
load_dotenv(find_dotenv())

#Get the database URI for envirement file > patch/.env
MONGO_URI = os.environ["MONGO_URI"]

try:
	print(f"{Fore.LIGHTYELLOW_EX} ~ Loading Database ~")
	#Connect to database
	Client = pymongo.MongoClient(MONGO_URI)
	print(f"{Fore.LIGHTMAGENTA_EX} • Database: {Fore.LIGHTGREEN_EX}Connected ✓")
except AttributeError as Error:
	print(f" • {Fore.LIGHTMAGENTA_EX}Database: {Fore.LIGHTRED_EX}Not Connect ×")

#Databases
database = Client[config["database_name"]]

#Collections
class db:
	users = database["users"]
	duels = database["duels"]
	settings = database["settings"]
	giveaway = database["giveaway"]
	cooldwons = database["cooldwons"]
	tournaments = database["tournaments"]
	suggetions = database["suggetions"]
	events = database["events"]
