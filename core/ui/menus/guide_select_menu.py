from nextcord.ext.commands import Bot
from nextcord import ButtonStyle, Interaction,  Embed, SelectOption
from nextcord.ui import Button, button, Modal, View, Select, TextInput
from random import choice
from Config import config, emojis
from core import stores, embeds

GuideItems = "- "

for i, val in stores.items.items():
	GuideItems += f"{val['name']}\n```{val['desc']}```\n- "

Guide = {
	"duels": "# Duel System™\n- كيف نلعب مباراة\n/duels create | لانشاء مباراة\n- طيب ماذا نفغل عندما افوز\n/duels accept | لتأكيد المباراة وتسجيل النتايج\nكل ما عليه فعله هو اإستخدام لامر من slash command ثم يحدد الفايز تاليه الخاسر\n- طيب ماذا لواردنا الغاء المباراة\n/duels delete | يمكنك انت او الاعب الثاني حذف المباراة في اي وقت\n- كيف نلعب  تحدي نقاط\n/duels create | ثم حدد خسمك وفي الخانة الثانية اضف عدد الناقط\n- هل يمكنني إنشاء  عددة مباريات في نفس الوقت\nيمكن االلعب وانشاء مباريات متعددة في نفس ضد اي لاعب طالما انه ليس نفس الاعب واذا اردة اللعب ضده مرة فيجب تاكيد المباراة الاولة او حذفها كما ذكر فوق",
	
	"points": "# Duel Points™\n- ماهي نقاط  المبارزة\nنقاط المبارزة هي نقاط تستخدم للعب تحديات ورفع مستوى الرنك كلما زادة نقاطك تزيد فرصتك في رفع مستوى الرنك\n- هل ممكن اجيب نقاط بدون لعب\nللحصول على النقاط يمكنك شراؤها من متجر النقاط `/store points` او يمكنك الحصول عليه من صندوق الهداية  اليومي او يمكنك شراء الصندوق الذي في المتجر الاغرض `/store items`\n- لو اردة لعب تحدي نقاط ولا ان اخسر نقاط ماذا افعل\nفي هذه الحالة تحتاج الى استخدام (قرص الامل) من المتجر يمكنك اللعب تحدي وضمان عدم نقص نقاطك في حال خسرت اي المباراة لمدة 12 ساعة\n- هل يمكنني مضاعفة نقاطي عند الفوز\nيمكنك مضاعفة نقاطك التي تفوز بها في التحديات وكذالك المشتريات لمدة 5 ساعة بواسطة (تنتين الذهبي) من المتجر\n",
	
	"store": f"# Store System\n- كيف اشتري من المتجر\n/store items | لشراء الايتمس\n/store points | لشراء نقاط \n- ما فائدة الايتمس\n{GuideItems} كيف افعل الايتمس\n/cards use\n- كيف اعرض اليتمس الخاصة بي\n/items show | يعرض جمع الآيتمس التي تملكها\n- كيف اطور الحقيبة حتى اقدر اخذن آيتمس اكثر\nاتشري (رفع المستوى ) الذي ذكر فوق"
}



class TheMenuSelect(Select):
	def __init__(self, author):
		super().__init__(
			placeholder="تفاصيل عن ؟",
			options=[
				SelectOption(label="نظام المبارزة", value="duels", emoji=emojis["duel"]),
				SelectOption(label="النقاط والرنك", value="points", emoji=emojis["points"]),
				SelectOption(label="المتجر والايتمس", value="store", emoji=emojis["buy"])
				
			]
		)
		self.author = author
	
	async def callback(self, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send("**منشن البوت اشان تظهر لك قائمة خاص بك **", ephemeral=True)
			return
		
		await interaction.message.edit(embed=embeds.embed(user=user, desc=Guide[self.values[0]], title="**• Bot Guide •**", icon_url=""))
		
		
class GuideMenuSelect(View):
	def __init__(self, author):
		super().__init__(timeout=None)
		self.add_item(TheMenuSelect(author=author))