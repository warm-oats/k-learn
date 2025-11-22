from discord.ext import commands
import discord
from discord import app_commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.deck_model import DeckModel
from view.deck_view import DeckView
from view.flashcard_view import FlashcardView
from database.db import Db

class DeckController(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self._bot = bot
        self._deck_model = DeckModel()
        self._deck_view = DeckView()
        self._flashcard_view = FlashcardView()
        self._db = Db()

    @app_commands.command(name = "get-deck-list", description = "Get list of all decks")
    async def get_deck_list(self, ctx: discord.Interaction):
        user_id = ctx.user.id
        user_name = ctx.user.name
        decks_info = self._deck_model.get_decks(user_id)

        # Defer due to fetching definitions can take long
        await ctx.response.defer(thinking = True)

        await self._deck_view.post_decks_info(decks_info, user_name, ctx)
    
    @app_commands.command(name = "create-deck", description = "Create new deck")
    @app_commands.describe(deck_name = "Name of new deck")
    async def add_deck(self, ctx: discord.Interaction, deck_name: str):
        
        # Defer due to fetching definitions can take long
        await ctx.response.defer(thinking = True)
        
        try:
            user_id = ctx.user.id

            self._db.create_deck(user_id, deck_name)

            await ctx.followup.send(content = f"Added deck '{deck_name}'")
        except ValueError as e:
            await ctx.followup.send(content = e)

    @app_commands.command(name = "study-deck", description = "Study a flashcard deck")
    @app_commands.describe(deck_name = "Name of deck to study")
    async def study_deck(self, ctx: discord.Interaction, deck_name: str):
        
        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)
        
        try:
            user_id = ctx.user.id
            flashcards_info = self._deck_model.get_vocabs(user_id, deck_name)

            await self._flashcard_view.post_flashcards_info(flashcards_info, deck_name, ctx)
        except ValueError as e:
            await ctx.followup.send(content = e)

    @app_commands.command(name = "delete-deck", description = "Delete a deck")
    @app_commands.describe(deck_name = "Deck name to be deleted")
    async def delete_deck(self, ctx: discord.Interaction, deck_name: str):
        
        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)
        
        try:
            user_id = ctx.user.id

            self._db.delete_deck(user_id, deck_name)


            await ctx.followup.send(content = f"Deleted deck '{deck_name}'")
        except ValueError as e:
            await ctx.followup.send(content = e)

    @app_commands.command(name = "update-deck-name", description = "Change deck name")
    @app_commands.describe(deck_name = "Current deck name", new_deck_name = "New name of deck")
    async def update_deck(self, ctx: discord.Interaction, new_deck_name: str, deck_name: str):

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        try:
            user_id = ctx.user.id

            self._db.update_deck_name(user_id, deck_name, new_deck_name)

            await ctx.followup.send(content = f"Changed deck '{deck_name}' to '{new_deck_name}'")
        except ValueError as e:
            await ctx.followup.send(content = e)

    @app_commands.command(name = "add-flashcard", description = "Add new flashcard")
    @app_commands.describe(deck_name = "Deck to add flashcard to", flashcard_front = "Front description of flashcard", flashcard_back = "Back description of flashcard")
    async def add_flashcard(self, ctx: discord.Interaction, deck_name: str, flashcard_front: str, flashcard_back: str):

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        try:
            user_id = ctx.user.id

            self._db.add_flashcard(user_id, deck_name, flashcard_front, flashcard_back)

            await ctx.followup.send(content = f"Added flashcard '{flashcard_front}' to deck '{deck_name}'")
        except ValueError as e:
            await ctx.followup.send(content = e)

    @app_commands.command(name = "delete-flashcard", description = "Delete a flashcard")
    @app_commands.describe(flashcard_name = "Name of flashcard to be deleted (front side)", deck_name = "Deck name storing this flashcard")
    async def delete_flashcard(self, ctx: discord.Interaction, flashcard_name: str, deck_name: str):

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        try:
            user_id = ctx.user.id

            self._db.delete_flashcard(user_id, deck_name, flashcard_name)

            await ctx.followup.send(content = f"Deleted flashcard '{flashcard_name}' from deck '{deck_name}'")
        except ValueError as e:
            await ctx.followup.send(content = e)

    @app_commands.command(name = "update-flashcard", description = "Update a flashcard's information")
    @app_commands.describe(flashcard_name = "Name of flashcard to be updated (front side)", 
                           deck_name = "Deck name storing this flashcard", 
                           flashcard_front = "New flashcard front side",
                           flashcard_back = "New flashcard back side")
    async def update_flashcard(self, ctx: discord.Interaction, flashcard_name: str, deck_name: str, flashcard_front: str = None, flashcard_back: str = None):

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        try:
            user_id = ctx.user.id

            if (not flashcard_front):
                flashcard_front = flashcard_name

            if (not flashcard_back):
                flashcard_back = self._db.fetch_flashcard_back(user_id, deck_name, flashcard_front)

            self._db.update_flashcard(user_id, deck_name, flashcard_name, flashcard_front, flashcard_back)

            await ctx.followup.send(content = f"Updated flashcard '{flashcard_name}' to {flashcard_front}: {flashcard_back} from deck '{deck_name}'")
        except ValueError as e:
            await ctx.followup.send(content = e)

async def setup(bot: commands.Bot):
    print("Inside deck controller setup function")
    await bot.add_cog(DeckController(bot))