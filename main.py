import discord
from datetime import datetime, timedelta
from discord.ext import commands

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def hilfe(ctx):
    embed = discord.Embed(title='Hilfe-Menü',
                          description='Hier sind einige verfügbare Befehle:',
                          color=discord.Color.blue())
    embed.add_field(name='1. !nachricht_mit_reaktion', value='Erstellt eine Nachricht mit einer Reaktion.', inline=False)
    embed.add_field(name='2. !ban', value='Bannt einen Benutzer.', inline=False)
    embed.add_field(name='3. !kick', value='Kickt einen Benutzer.', inline=False)
    embed.add_field(name='4. Hilfe benötigt?', value='Wende dich an das höhere Team oder die Entwickler.', inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user.name} ({bot.user.id})')

@bot.command()
async def nachricht_mit_reaktion(ctx):
    nachricht = await ctx.send('Testnachricht')
    await nachricht.add_reaction('👍')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    nachricht_id = payload.message_id
    reaktion = payload.emoji.name
    rolle_id = 1117211428277997578

    if reaktion == '👍':
        guild = bot.get_guild(payload.guild_id)
        rolle = guild.get_role(rolle_id)
        member = guild.get_member(payload.user_id)

        if member is not None and rolle is not None:
            await member.add_roles(rolle)
            print(f'Benutzer {member.name} hat die Rolle {rolle.name} erhalten!')

@bot.command()
async def ban(ctx, member: discord.Member, duration: int, *, reason: str):
    # Dauer in Stunden in ein timedelta-Objekt umwandeln
    ban_duration = timedelta(hours=duration)

    # Zeitpunkt des Bans
    ban_start = datetime.now()

    # Zeitpunkt des Ban-Endes berechnen
    ban_end = ban_start + ban_duration

    # Benutzer bannen
    await member.ban(reason=reason)

    # Bann-Informationen in einer Embed-Nachricht anzeigen
    embed = discord.Embed(title='Benutzer-Bann',
                          description=f'{member.mention} wurde gebannt.',
                          color=discord.Color.red())
    embed.add_field(name='Dauer', value=f'{duration} Stunden')
    embed.add_field(name='Grund', value=reason)
    embed.add_field(name='Ban-Start', value=ban_start.strftime('%Y-%m-%d %H:%M:%S'))
    embed.add_field(name='Ban-Ende', value=ban_end.strftime('%Y-%m-%d %H:%M:%S'))

    await ctx.send(embed=embed)


bot.run('Token')
