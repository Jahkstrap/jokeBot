import config
import discord
import spacy
from discord.ext import commands

TOKEN = config.DISCORD_TOKEN
bot = commands.Bot(command_prefix='!')

nlp = spacy.load("en_core_web_sm")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def joke(ctx, *, sentence: str = None):
    # If the command is replying to a message, use the content of the replied message as input
    if ctx.message.reference:
        replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
        sentence = replied_message.content
    
    if not sentence:
        await ctx.send("Please provide a sentence or reply to a message!")
        return

    doc = nlp(sentence)

    # Find verbs and nouns from the sentence
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]

    if not verbs or not nouns:
        await ctx.send("Couldn't find enough verbs or nouns in the sentence!")
        return

    # Create the joke
    joke_msg = f"She {verbs[0]} on my {nouns[0]} until I {verbs[-1] if len(verbs) > 1 else verbs[0]}"
    await ctx.send(joke_msg)

bot.run(TOKEN)