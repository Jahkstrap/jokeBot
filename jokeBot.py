import random
import config
import discord
import spacy
from discord.ext import commands

TOKEN = config.DISCORD_TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

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

    # Randomly choose a verb and noun
    chosen_verb = random.choice(verbs)
    chosen_noun = random.choice(nouns)
    
    # If there's more than one verb, pick another one that isn't the chosen_verb for the punchline
    if len(verbs) > 1:
        second_verb = random.choice([v for v in verbs if v != chosen_verb])
    else:
        second_verb = chosen_verb

    # Create the joke
    if chosen_verb.endswith('ing'):
        joke_msg = f"She is {chosen_verb} on my {chosen_noun} until I {second_verb}"
    else:
        joke_msg = f"She {chosen_verb} on my {chosen_noun} until I {second_verb}"
    
    await ctx.send(joke_msg)

bot.run(TOKEN)