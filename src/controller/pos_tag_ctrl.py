from discord.ext import commands
from pathlib import Path
from discord import app_commands
import discord
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.pos_tag_model import PosTagModel
from view.pos_tag_view import PosTagView

class PosTagController(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._pos_tag_model = PosTagModel()
        self._pos_tag_view = PosTagView()
    
    @app_commands.command(name = 'extract-pos', description = 'Extract Korean sentence parts of speech in context')
    @app_commands.describe(sentence = "Korean sentence(s)", colorize = "Colorize all parts of speech")
    async def extract_pos(self, ctx: discord.Interaction, *, sentence: str, colorize: bool = False):

        # Defer due to fetching translations can take long
        await ctx.response.defer(thinking = True)

        # Contains mapping of pos: [words] pairs
        pos_tag_map = self._pos_tag_model.extract_pos(sentence)

        # Contains sentence, translation, and POS map
        translation_package = self._pos_tag_model.map_pos_meaning(sentence, pos_tag_map)

        # POS mapping of smallest unit of word in sentence for colorization
        no_stem_words = self._pos_tag_model.extract_pos(sentence, True, False)

        await self._pos_tag_view.post_tag_info(ctx, translation_package, no_stem_words, colorize)

async def setup(bot: commands.Bot):
    print("Inside pos tag controller setup function")
    await bot.add_cog(PosTagController(bot))