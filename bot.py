import discord
from discord.ext import commands
import logging
from pathlib import Path 
import json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

secret_file = json.load(open(cwd+'/secrets.json'))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    print(f"-----\nLogged in successfully.\n-----\nName : {bot.user.name}\nID : {bot.user.id}\nCurrent prefix : .\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Listening to .help"))

#HELP COMMAND
bot.remove_command("help")
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="Help",description="Use .help <command> for more information on a command.",color=ctx.author.color)
    em.add_field(name="__**Fun**__", value="hi, say")
    em.add_field(name="__**Moderation**__", value="purge")
    em.add_field(name="__**Bot**__", value="info")
    await ctx.send(embed=em)

@help.command() #hi
async def hi(ctx):
    em = discord.Embed(title="Hi", description="Greets the user with a Hello", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".hi or .hello or .hey")
    await ctx.send(embed=em)

@help.command() #say
async def say(ctx):
    em = discord.Embed(title="Say", description="Repeats the text entered by the user.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".say <*text to be repeated*>")
    await ctx.send(embed=em)

@help.command() #purge
async def purge(ctx):
    em = discord.Embed(title="Purge", description="Purges the specified number of messages. (Limit - 1000)", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".purge <*number of messages to be deleted*>")
    em.add_field(name="Default", value="If the number of messages to be deleted is not provided, 5 messages will be deleted by default.")
    await ctx.send(embed=em)

@help.command() #info
async def info(ctx):
    em = discord.Embed(title="Info", description="Shows the bot's general information.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".info")
    await ctx.send(embed=em)
    
#HI COMMAND
@bot.command(name='hi', aliases=['hello','hey'])   
async def _hi(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")

#ECHO COMMAND
@bot.command()    
async def say(ctx, *, message=None):
      message = message or "Please provide the message to be repeated."
      await ctx.message.delete()
      await ctx.send(message)

#PURGE COMMAND
@bot.command(pass_context=True)
async def purge(ctx, limit=5):
        if(0<limit<=1000):
            await ctx.channel.purge(limit=limit+1)
            await ctx.message.delete()
        elif(limit==0):
            await ctx.send(f"How tf can you delete 0 messages!?")
        elif(limit>1000):
            await ctx.send(f"Cannot delete more than 1000 messages.")
        else:
            await ctx.send(f"Invalid argument.")

#INFO COMMAND
@bot.command()
async def info(ctx):
    dpyversion = discord.__version__
    serverCount = len(bot.guilds)
    membercount = len(set(bot.get_all_members()))
    em = discord.Embed(title="Bot Info:", description=f"I am in {serverCount} servers with a total of {membercount} members.", color=ctx.author.color)
    em.add_field(name="discord.py version:", value=f"{dpyversion}", inline=False)
    em.add_field(name="Made by:", value="INFERNO#1043", inline=False)
    await ctx.send(embed=em)

#LOGOUT COMMAND
@bot.command(aliases=['disconnect','shutdown'])
@commands.is_owner()
async def logout(ctx):
    await ctx.send("Logging out... :wave:")
    await bot.logout()

@logout.error
async def logout_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Hey, {ctx.author.mention}! You do not have the permission to run this command, as you are not the bot owner.")
    else:
        raise error
        

bot.run(bot.config_token)