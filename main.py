import discord
from discord.ext import commands
import logging
from pathlib import Path 
import datetime
import aiohttp
import requests
import os
from discord import app_commands
from dotenv import load_dotenv


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")  


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix = ".", intents=intents)

    async def setup_hook(self):
        await self.tree.sync(guild= discord.Object(id=guildId))
        print(f"-----\nSlash commands have synced.\nBooting up the bot...\n-----")

bot = Bot()
load_dotenv()

bot.config_token = os.getenv('TOKEN')
logging.basicConfig(level=logging.INFO)




@bot.event
async def on_ready():
    print(f"-----\nBot booted up successfully.\n-----\nName : {bot.user.name}\nCurrent prefix : .\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Listening to .help"))
    bot.started = datetime.datetime.now()

#definitions
bot.uptime = datetime.datetime.utcnow()
guildId = 838611549894475777


#APP COMMANDS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@bot.tree.context_menu(name='Hi', guild= discord.Object(id=guildId))
async def hello(interaction: discord.Integration, message: discord.Message):
    await interaction.response.send_message("Hellu")


#HYBRID HI COMMAND
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
async def on_command_error(self,ctx,error):
    await ctx.reply(error, ephemeral=True)


@bot.hybrid_command(name = "hi", with_app_command = True, description = "Greets the user.")
@app_commands.guilds(discord.Object(id=guildId))
async def test(ctx: commands.Context):
    await ctx.defer(ephemeral=False)
    await ctx.reply(f"Hello, {ctx.author.mention}!")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#SAY COMMAND
@bot.command()    
async def say(ctx, *, message=None):
      message = message or "Please provide the message to be repeated."
      await ctx.message.delete()
      await ctx.send(message)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#PURGE COMMAND
@bot.command()
async def purge(ctx, limit=5, member: discord.Member=None):
    await ctx.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await ctx.send("Please pass in an integer as limit.")
    if not member:
        await ctx.channel.purge(limit=limit)
        em = discord.Embed(title=f"Purged {limit} messages.", color=ctx.author.color)
        return await ctx.send(embed=em, delete_after=5)
    async for m in ctx.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await ctx.channel.delete_messages(msg)
    await ctx.send(f"Purged {limit} messages of {member.name}.", delete_after=5)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#INFO COMMAND
@bot.command()
async def info(ctx):
    dpyversion = discord.__version__
    serverCount = len(bot.guilds)
    membercount = len(bot.users)
    em = discord.Embed(title="Bot Info:", description=f"I am in {serverCount} servers with a total of {membercount} members.", color=ctx.author.color)
    em.add_field(name="discord.py version:", value=f"{dpyversion}", inline=False)
    em.add_field(name="Made by:", value="INFERNO#1043", inline=False)
    await ctx.send(embed=em)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#LOGOUT COMMAND
@bot.command(aliases=['shutdown'])
@commands.is_owner()
async def logout(ctx):
    em = discord.Embed(title="Signing out!", color=discord.Colour.gold())
    em.set_image(url="https://media.tenor.com/QV8FWvZoGp0AAAAi/canard-bye.gif")
    await ctx.send(embed=em)
    await ctx.bot.close()

@logout.error
async def logout_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Hey, {ctx.author.mention}! You do not have the permission to run this command, as you are not the bot owner.")
    else:
        raise error

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#PING COMMAND
@bot.hybrid_command(name = "ping", with_app_command = True, description = "Shows the latency of the bot.")
@app_commands.guilds(discord.Object(id=guildId))
async def test(ctx: commands.Context):
    await ctx.defer(ephemeral=True)
    await ctx.reply(f"Pong! `{round(bot.latency * 1000)}ms`")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#UPTIME COMMAND
@bot.command()
async def uptime(ctx):
    uptime = int(bot.started.timestamp())
    await ctx.send(f"Last Reboot: <t:{uptime}:R>")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#DUCK COMMAND
@bot.command()
async def duck(ctx):
    url = "https://random-d.uk/api/v2/random"
    r = requests.get(url)
    r = r.json()
    print(r)
    embed = discord.Embed()
    embed = discord.Embed(title="Quack!", color=discord.Color.gold())
    embed.set_image(url=r['url'])
    await ctx.channel.send(embed=embed)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#MUTE COMMAND
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild=ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True)

    await member.add_roles(mutedRole, reason=reason)
    em = discord.Embed(title=f"{member.name} was muted.", description=f"**Reason**: {reason}.",colour=discord.Colour.gold())
    await ctx.send(embed=em)
    await member.send(f"You have been muted in **{guild.name}**. \nReason: {reason}.")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#UNMUTE COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   await member.remove_roles(mutedRole)
   embed = discord.Embed(title=f"{member.name} has been unmuted.",colour=discord.Colour.gold())
   await member.send(f" You have been unmuted from **{ctx.guild.name}**.")
   await ctx.send(embed=embed)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#KICK COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(title=f" You were kicked from **{ctx.guild.name}**.", description=f"{reason}", colour=discord.Colour.gold())
    await member.send(embed=embed)
    await member.kick(reason=reason)
    embed = discord.Embed(title=f"{member.name} was kicked.", colour=discord.Colour.gold())
    await ctx.send(embed=embed)
   

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#BAN COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(title=f" You were banned from **{ctx.guild.name}**.", description=f"{reason}", colour=discord.Colour.gold())
    await member.send(embed=embed)
    await member.ban(reason=reason, delete_message_days=1)
    em = discord.Embed(title=f"{member.name} was banned.", description=f"{reason}", colour=discord.Colour.gold())
    await ctx.send(embed=em)
   

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#UNBAN COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, user: discord.User, *, reason=None):
   await ctx.guild.unban(user, reason=reason)
   embed = discord.Embed(title=f"{user.name} was unbanned.", description=f"{reason}", inline=True, colour=discord.Colour.gold())
   await ctx.send(embed=embed)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#NICKNAME COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    em=discord.Embed(title="Nickname changed.", color=discord.Colour.gold())
    await ctx.send(embed=em)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#ADDROLE COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, member: discord.Member, role):
    Role = discord.utils.get(ctx.guild.roles, name=role)
    await member.add_roles(Role)
    em=discord.Embed(title="Role added.", color=discord.Colour.gold())
    await ctx.send(embed=em)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#REMOVEROLE COMMAND
@bot.command()
@commands.has_permissions(administrator=True)
async def rrole(ctx, member: discord.Member, role):
    Role = discord.utils.get(ctx.guild.roles, name=role)
    await member.remove_roles(Role)
    em=discord.Embed(title="Role Removed.", color=discord.Colour.gold())
    await ctx.send(embed=em)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#AVATAR COMMAND
@bot.command(aliases=['avatar'])
async def av(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar.url
    em = discord.Embed(title=f"{member.name}'s avatar:", color=discord.Colour.gold())
    em.set_image(url=userAvatar)
    await ctx.send(embed=em)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


#HELP COMMAND
bot.remove_command("help")
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="**Help**",description="Use `.help <command>` for more information on a command.",color=ctx.author.color)
    em.add_field(name="__**Fun**__", value="`hi`, `say`, `duck`, `avatar`", inline=False)
    em.add_field(name="__**Moderation**__", value="`purge`, `mute`, `unmute`, `kick`, `ban`, `unban`, `nick`, `addrole`, `rrole`", inline=False)
    em.add_field(name="__**Bot**__", value="`info`, `ping`, `uptime`", inline=False)
    em.set_thumbnail(url='https://cdn.discordapp.com/attachments/917409223359496204/924625506664587264/1a8d4f10db33ebddf64e183fa025c196.jpg')
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
    em.add_field(name="**Syntax**", value=".purge [count]\n.purge [count] [user]")
    em.add_field(name="Default", value="If the number of messages to be deleted is not provided, 5 messages will be deleted by default.")
    await ctx.send(embed=em)

@help.command() #info
async def info(ctx):
    em = discord.Embed(title="Info", description="Shows the bot's general information.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".info")
    await ctx.send(embed=em)

@help.command() #ping
async def ping(ctx):
    em = discord.Embed(title="Ping", description="Shows the bot's latency.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".ping")
    await ctx.send(embed=em)

@help.command() #uptime
async def uptime(ctx):
    em = discord.Embed(title="Uptime", description="Shows the bot's uptime", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".uptime")
    await ctx.send(embed=em)

@help.command() #duck
async def duck(ctx):
    em = discord.Embed(title="Duck", description="Sends random duck images.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".duck")
    await ctx.send(embed=em)

@help.command() #mute
async def mute(ctx):
    em = discord.Embed(title="Mute", description="Mutes the mentioned user.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".mute [user] <reason>")
    em.set_footer(text="Use .unmute command to unmute the user.")
    await ctx.send(embed=em)

@help.command() #unmute
async def unmute(ctx):
    em = discord.Embed(title="Unmute", description="Unmutes the mentioned user.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".unmute [user]")
    await ctx.send(embed=em)

@help.command() #kick
async def kick(ctx):
    em = discord.Embed(title="Kick", description="Kicks the mentioned member from the server.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".kick [user] <reason>")
    await ctx.send(embed=em)

@help.command() #ban
async def ban(ctx):
    em = discord.Embed(title="Ban", description="Bans the mentioned member from the server.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".ban [user] <reason>")
    em.set_footer(text="Use .unban command to unmute the user.")
    await ctx.send(embed=em)

@help.command() #unban
async def unban(ctx):
    em = discord.Embed(title="Unban", description="Revokes the member's ban.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".unban [user_id]")
    await ctx.send(embed=em)

@help.command() #nick
async def nick(ctx):
    em = discord.Embed(title="Nick", description="Changes the nickname of the mentioned user.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value=".nick [user] <new nickname>")
    await ctx.send(embed=em)

@help.command() #addrole
async def addrole(ctx):
    em = discord.Embed(title="Addrole", description="Adds the mentioned role to the user.", color=ctx.author.color)
    em.set_footer(text="Example: .addole @Jack Members")    
    em.add_field(name="**Syntax**", value="`.addrole [user] [role]`")
    await ctx.send(embed=em)

@help.command() #rrole
async def rrole(ctx):
    em = discord.Embed(title="RemoveRole", description="Removes the mentioned role from the user.", color=ctx.author.color)
    em.set_footer(text="Example: .rrole @Jhon Members")
    em.add_field(name="**Syntax**", value="`.rrole [user] [role]`")
    await ctx.send(embed=em)

@help.command() #avatar
async def avatar(ctx):
    em = discord.Embed(title="Avatar", description="Sends the profile picture of the user in an embed form.", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="`.avatar [user]` or `.av [user]`")
    await ctx.send(embed=em)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
bot.run(bot.config_token)
