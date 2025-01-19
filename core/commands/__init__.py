import asyncio
from .others import OthersCommands
from .system import SystemCommands
from .moderation import Moderation
from .cards_system import CommandCardsSystem

class cmds:
	def __init__(self, bot):
		self.bot = bot
		self.others = OthersCommands(bot)
		self.system = SystemCommands(bot)
		self.moderation = Moderation(bot)
		self.cards = CommandCardsSystem(bot)


	