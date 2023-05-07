import discord
from dotenv import load_dotenv
import os
from discord.enums import ChannelType
import asyncio

from app.summarize_script.summarize import csv_data_from_pdf_bytes


load_dotenv()

bot = discord.Bot()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

threads = {}

def make_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Bot(intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    return bot

class ProfessorCog(discord.Cog):

    def __init__(self, bot:discord.Bot):
        self._bot = bot
        self.thread = None
        self.professor = None

    @discord.slash_command(description = 'practice new interview', name = 'test')
    async def work(self, ctx, role: discord.Option(str)): # a slash command will be created with the name "ping"

        self.thread = await ctx.channel.create_thread(name="new interview", type=ChannelType.public_thread)
        await ctx.respond('created new interview thread')
        await self.thread.send(f'Commencing {role} interview, say hi!')    

    @discord.slash_command(description = "generate summary for script", name = "summarize")
    async def summarize(self, ctx, file: discord.Attachment) :
        file_bytes = await file.read()
        
        await ctx.respond('processing file')
        thread = await ctx.channel.create_thread(name="summarizing file", type=ChannelType.public_thread)

        summary_csv = await csv_data_from_pdf_bytes(file_bytes, thread)
        f = discord.File(summary_csv, filename='best_name_ever.csv')

        await thread.send(file = f)



    @discord.Cog.listener()
    async def on_message(self, message):
        # Make sure we won't be replying to ourselves.
        if message.author.id == self._bot.user.id:
            return

        if not message.channel.id == self.thread.id:
            return

        await message.channel.send('message')


async def main():
    bot = make_bot()
    bot.add_cog(ProfessorCog(bot))
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())