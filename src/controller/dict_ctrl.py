from discord.ext import commands
import discord
from discord import app_commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.dict_model import DictModel
from view.dict_view import DictView
from view.button_view import DirectionalButtonView

class DictController(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self._bot = bot
        self._dict_model = DictModel()
        self._dict_view = DictView()

    @app_commands.command(name = "define", description = "Define English word")
    @app_commands.describe(word = "English word")
    async def define_word(self, ctx: discord.Interaction, word: str):
        pos_contexts = self._dict_model.get_word_info(word) 
        button_view = DirectionalButtonView(pos_contexts, self._dict_view.edit_word_info)

        # Defer due to fetching definitions can take long
        await ctx.response.defer(thinking = True)

        await self._dict_view.post_word_info(ctx, pos_contexts, button_view)

async def setup(bot: commands.Bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))