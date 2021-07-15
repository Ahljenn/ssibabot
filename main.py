import discord
import locale
import os
import math
import datetime
import asyncio
import pandas
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive
from pet import get_petites
from pet import get_blacks
client = commands.Bot(command_prefix = ';',help_command=None) 
locale.setlocale(locale.LC_ALL, '') 
siba_img = 'https://cdn.discordapp.com/attachments/838627115326636082/845048535023747102/image0.jpg'
siba_img_landscape = 'https://cdn.discordapp.com/attachments/836716455072235541/845093553821581363/siba.jpg'
flag_times_utc = [11,18,20,21,22] #time-1 
equip_types = ['abso','book','eyepatch','arcane','cra','gollux','pap','sw']
checklist_items = ['Legion setup','Link skills','Hyper skills/stats', 'Buff freezers', 'Familiars','Pets/pet food','Bossing equips/rings','Green bind', 'Nodes','Monster park extreme potions','Guild skills','Guild blessing','Ursus','Cold winter/HT/apple/tengu buffs','Candied apples','Level 250/275 Fame buff','Boss rush pots','Alchemy stat potion I - X','MVP superpower','Echo','Familiars setup','Weapon tempering']

async def build_string(items):
  ss = '' 
  for item in items:
    ss += '- '+ item + '\n'
  return ss

async def get_value(file_path, flame_score):
  """Returns expected number of flames required given the file_path and flame_score."""
  expected_values = pandas.read_csv(file_path,
                                    index_col=0,
                                    names=['Flame score','Expected number of flames'])
  return math.floor(expected_values.iat[flame_score,0])

@client.command()
async def flame(ctx, equip_type='', flame_score=0):
  """Returns average number of eternal flames to beat flame_score on equip_type."""
  value = int()
  try:
    if flame_score < 0:
      raise IndexError
    if any(equip_type == equip for equip in equip_types):
      if equip_type == 'abso' or equip_type == 'book' or equip_type == 'eyepatch':
        value = await get_value('./csv/absolab-spellbook-eyepatch.csv', flame_score)
      elif equip_type == 'arcane':
        value = await get_value('./csv/arcane.csv', flame_score)
      elif equip_type == 'cra':
        value = await get_value('./csv/cra.csv',flame_score)
      elif equip_type == 'gollux':
        value = await get_value('./csv/gollux.csv', flame_score)
      elif equip_type == 'pap':
        value = await get_value('./csv/pap.csv', flame_score)
      elif equip_type == 'sw':
        value = await get_value('./csv/sw.csv', flame_score)
      await ctx.send(f'{value:,} average flame(s) to hit.')
    else:
      raise TypeError
  except IndexError:
    await ctx.send('Invalid range. Refer to ;flame-info for valid ranges.')
  except TypeError:
    await ctx.send('Invalid equip. Refer to ;flame-info for equips supported.')

@client.command()
async def vac(ctx, n):
  """Returns the results of obtaining n Petite Luna Pets"""
  try:
    n = int(n)
    if n > 20:
      raise IndexError
    if n < 1:
      raise ValueError
    results = get_petites(n) #variable that holds a list of items
    embed = discord.Embed(
      title = 'Vac Pets',
      description = f'Results of obtaining **{n}** Petite Luna Pet(s)',
      colour = discord.Colour.random()
    )
    embed.set_footer(text='Powered by 씨발')
    embed.set_thumbnail(url='https://www.freeiconspng.com/thumbs/eggplant-png/high-resolution-eggplant-png-clipart-3.png')
    for i, (k,v) in  enumerate (results.items()):
      if i > 0:
        if(i == 1 or i == 3 or i == 4):
          embed.add_field(name=k,value = f'```{v} NX/MP```',inline=False)
        else:
          embed.add_field(name=k,value = f'```{v} mesos```',inline=False)
    await ctx.send(embed=embed)
  except ValueError:
    await ctx.send(f'Invald number of Petite Luna Pets to go for: {n}')
  except IndexError:
     await ctx.send('National Gambling Hotline: 1-800-522-4700')

@client.command()
async def black(ctx, n):
  """Returns results of obtaining n Wonder Black Luna Pet(s)"""
  try:
    n = int(n)
    if n > 20:
      raise IndexError
    if n < 1:
      raise ValueError
    results = get_blacks(n)
    embed = discord.Embed(
      title = 'Wonder Black Pets',
      description = f'Results of obtaining **{n}** Wonder Black Pets',
      colour = discord.Colour.random()
    )
    embed.set_footer(text='Powered by 씨발')
    embed.set_thumbnail(url='https://www.freeiconspng.com/thumbs/eggplant-png/high-resolution-eggplant-png-clipart-3.png')
    for i, (k,v) in  enumerate (results.items()):
      if i > 0:
        if i == 1:
          embed.add_field(name=k,value = f'```{v} packages```',inline=False)
        elif(i == 3 or i == 4):
          embed.add_field(name=k,value = f'```{v} NX/MP```',inline=False)
        else:
          embed.add_field(name=k,value = f'```{v} mesos```',inline=False)
    await ctx.send(embed=embed)
  except ValueError:
    await ctx.send(f'Invald number of Petite Luna Pets to go for: {n}')
  except IndexError:
    await ctx.send('National Gambling Hotline: 1-800-522-4700')

@client.command(name='flame-info')
async def flame_info(ctx):
  """Returns an embed with flame information, providing associated score ranges, equip names."""
  embed = discord.Embed(
    title = 'Flame information',
    description = ';flame command parameter details',
    colour = discord.Colour.blue(),
    timestamp=datetime.datetime.utcnow()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/697998173888708652/706341428896203144/image0.png')
  embed.add_field(name='Equip (exact) names',value='abso, book, eyepatch, arcane, cra, gollux, pap, sw',inline=False)
  embed.add_field(name='Ranges for each equip',value='gollux: 0-115\nsw: 0-120\npap: 0-160\ncra: 0-160\nabso: 0-180\nbook: 0-180\neyepatch: 0-180\narcane: 0-210',inline=False)
  await ctx.send(embed=embed)

time = datetime.datetime.now
async def timer():
  """Timer set for flag race pings."""
  msg_sent = False
  while not client.is_closed():
    if any(time().hour == flag for flag in flag_times_utc) and time().minute == 50:
      #checks if current time is flag race time from list
      if not msg_sent:
        channel = client.get_channel(530284491319672853) 
        #get guild-content channel id and flag_role
        flag_role = get(channel.guild.roles, name = 'Flag Race')

        embed = discord.Embed( #first embed for ping 1
          title = 'Flag Race',
          description = 'Flag race will be starting in about 10 minutes.',
          colour = discord.Colour.blue(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text='Powered by 씨발')
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Blue_flag_waving.svg/951px-Blue_flag_waving.svg.png')
        embed.set_author(name='씨바-bot')
        await channel.send(f'{flag_role.mention} in 10',embed=embed)
        await asyncio.sleep(9*60) #wait 9 minutes

        embed2 = discord.Embed( #second embed for ping 2
          title = 'Flag Race',
          description = 'Flag race is starting soon, get ready. Make sure you are in a map where you can recieve the invitiation.',
          colour = discord.Colour.red(),
          timestamp=datetime.datetime.utcnow()
        )
        embed2.set_footer(text='Powered by 씨발')
        embed2.set_thumbnail(url='https://webstockreview.net/images/cone-clipart-triangle-8.png')
        embed2.set_author(name='씨바-bot')
        await channel.send(f'{flag_role.mention} in 1',embed=embed2)
        msg_sent = True
      else:
        msg_sent = False
    await asyncio.sleep(1) 

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you sleep | ;help'))
    client.loop.create_task(timer())
    print('Bot is deployed...')

@client.command()
async def help(ctx):
  """"Help function provided to the user."""
  embed = discord.Embed(
    title = 'Help',
    description = '씨바-bot Help Library. These are the following commands everyone can use in this server currently. (The prefix to use commands is ";") Note that the commands are case-sensitive. More functionalities will be added overtime.',
    colour = discord.Colour.purple()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_image(url=siba_img_landscape)
  embed.set_author(name='씨바-bot')

  embed.add_field(name='General Commands',value='\u200b', inline=False)
  embed.add_field(name=';checklist',value='View the pre-run checklist that you should go through prior to runs', inline=False)
  embed.add_field(name=';sale <meso amount> <party size> <mvp status>',value='Calculate sale given initial amount, number of members, and mvp status. e.g: ```;sale 1,800,000,000 4```\nIf you have **MVP**, add a 1 to the end parameter (decreased tax). e.g: ```;sale 1,800,000,000 4 1```', inline=False)

  #Flame fields
  embed.add_field(name=';flame <equip> <score>',value='Prints average number of eternal flames required to beat *score.* e.g: ```;flame gollux 70```',inline=False)
  embed.add_field(name=';flame-info',value='View information for flame commands.',inline=False)

  #Vac fields
  embed.add_field(name =';vac <n>',value= 'View the results of obtaining the given amount of *Petite Lunas.* (1-20) e.g: ```;vac 10```',inline=True)
  embed.add_field(name =';black <n>',value= 'View the results of obtaining the given amount of *Wonder Black Lunas.* (1-20) e.g: ```;black 10```',inline=True)


  await ctx.send(embed=embed)

@client.command()
async def sale(ctx,capital,pty=1,mvp=0):
  """Returns the amount of capital for a given sale with initial amount, party members, and mvp status."""
  try:
    capital = int(capital.replace(',',''))
    if capital <= 0 or pty <= 1:
      raise ValueError
    tax = 0.03 if mvp else 0.05
    amt = math.floor(capital * (1 -  tax) / (pty - 0.05))
    sale = f'```{amt:,} mesos each```'
    embed = discord.Embed(
      title = 'Sale amount',
      description = sale,
      colour = 0xFFFF00
    )
    embed.set_footer(text='Powered by 씨발')
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/617213926723158056.png?v=1')
    await ctx.send(embed=embed)
  except ValueError:
    await ctx.send('Invalid parameters used. (Type ;help for more information)')

@client.command()
async def checklist(ctx):
  """Returns boss run checklist to user in an embed."""
  embed = discord.Embed(
    title = 'Pre-run Checklist',
    description = 'Make sure everything is set and ready to go, prior to the boss runs.',
    colour = discord.Colour.blue()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/thin-line-color-2/21/27-512.png')
  checklist = await build_string(checklist_items)
  embed.add_field(name='Please check the following items:',value=checklist,inline=False)
  await ctx.send(embed=embed)

@client.command()
async def schedule(ctx):
  """Returns schedule for party 1 and party 2"""
  embed = discord.Embed(
    title = 'Schedule',
    description = 'Below are the usual times Chilly line and Dan line will run. The run times are tentative - subject to change.',
    colour = discord.Colour.blue()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://students.wustl.edu/wp-content/uploads/2018/08/Schedule.png')
  embed.set_author(name='씨바-bot')
  embed.add_field(name='Boss Runs [Friday/Saturday]: ',value='8:30PM (PST) | 11:30 PM (EST) | 10:30AM (1 day ahead: AEST)', inline=False)
  embed.add_field(name='GPQ [Sunday]: ',value='7:00PM (PST) | 10:00 PM (EST) | 11:00AM (Monday: AEST)', inline=False)
  await ctx.send(embed=embed)


@client.command(name='ping')
@commands.has_any_role('Developer','Board of Directors','administrator')
async def ping_party(ctx):
  """Returns an embed and pings party 1 and party 2"""
  await checklist(ctx)
  team1 = get(ctx.guild.roles, name = 'Team 1')
  team2 = get(ctx.guild.roles, name = 'Team 2')
  
  embed = discord.Embed(
    title = 'Run Reminder',
    description = 'Don\'t forget we are running later tonight. Refer up above for the usual run times for each party. The run times are tentative - subject to change. Message your respective party leaders if there are any changes that need to be made.',
    colour = discord.Colour.red()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://webstockreview.net/images/cone-clipart-triangle-8.png')
  await ctx.send(embed=embed)
  await ctx.send(f'{team1.mention,team2.mention}')

#check message
@client.event
async def on_message(message):
  if message.author != client.user: #if not the bot
    if message.content.lower() in ['gary','yena','sus']:
      await message.channel.send('sus')
    if message.content.lower() in ['kevin','kev','<:boomerKevin:859524709146165338>']:
      await message.channel.send('<:kevin:845474836271595530>')
    if message.content.lower() in ['ssibal','sibal','sibai','ssibai']:
      await message.channel.send('noma')
    if message.content in ['<:Wall:818644951012474901>']:
      await message.channel.send('<:Wall:818644951012474901>')
    await client.process_commands(message)

keep_alive() 
client.run(os.environ['token'])