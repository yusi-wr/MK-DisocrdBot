from random import choice, choices, randint
from Config import config, emojis
from nextcord import Interaction, Embed, Member, Color
import humanfriendly
import time
from core.ui import buttons
from .cards import Card
from .collections import cards_data, cards_art, cards_name

def game_embed(
	correct_name,
	desc,
	guild,
	user: Member
	):
	
	times = humanfriendly.parse_timespan("30s")
	end = time.time() + times
	color = Color.random()
	card_id = Card(cards_data[correct_name], guild).id
	image = cards_art[card_id]["url"]
	embed = Embed(color=color)
	embed.description = f">>> **{desc}**" + f"\n- {emojis['time']} <t:{int(end)}:R>"
	embed.set_image(url=image)
	embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
	
	return embed	

#game function
async def CardsGame(
   interaction: Interaction,
   CountAnswer = 0,
   points = 0,
   round = 0,
   archetype: list = None
	):
		user = interaction.user
		guild = interaction.guild
		result_q = randint(5, 8)
		if archetype:
			names_list = choices(archetype, k=result_q)
		else:
			names_list = choices(cards_name, k=result_q)
		
		correct_name = choice(names_list)
		
		embed = game_embed(
				correct_name=correct_name,
				desc="أي زر هو الإسم الصحيح لهذه البطاقة\n-------------\n- الجولة: {roundicon} {round}\n- الاجابات الصحيحة: {answericon} {answer}\n- الفضة: {gemsicon} {gems}".format(
				 	answericon=emojis["pointer"],
				 	roundicon=emojis["pointer"],
				 	gemsicon=emojis["coins"],
				 	round=round,
				 	answer=CountAnswer,
				 	gems=f"${points:,}",
					),
				guild=guild,
				user=user
				)
		view=buttons.CardsGameButton(
			origin_inter=interaction,
			names=names_list,
			CountAnswer=CountAnswer,
			points=points,
			round=round,
			correct_name=correct_name,
			fromArchetype=archetype
		)
		msg = await interaction.followup.send(embed=embed, view=view)
		view.message = msg
