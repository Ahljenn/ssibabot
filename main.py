import discord
import locale
import os
import math
import datetime
import asyncio
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive 
client = commands.Bot(command_prefix = ';',help_command=None) 
locale.setlocale(locale.LC_ALL, '') 

siba_img = 'https://cdn.discordapp.com/attachments/838627115326636082/845048535023747102/image0.jpg'
siba_img_landscape = 'https://cdn.discordapp.com/attachments/836716455072235541/845093553821581363/siba.jpg'
flag_times_utc = [11,18,20,21,22] #time-1 for 1 hour before

time = datetime.datetime.now

#function timer to send msg at set times
async def timer():
  msg_sent = False
  while not client.is_closed():
    if any(time().hour == flag for flag in flag_times_utc) and time().minute == 50:
      if not msg_sent:
        channel = client.get_channel(530284491319672853)
        flag_role = get(channel.guild.roles, name = 'Flag Race')

        embed = discord.Embed( #first embed for first ping
          title = 'Flag Race',
          description = 'Flag race will be starting in about 10 minutes.',
          colour = discord.Colour.blue(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text='Powered by 씨발')
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Blue_flag_waving.svg/951px-Blue_flag_waving.svg.png')
        embed.set_author(name='씨바-bot')
        await channel.send(f'{flag_role.mention} in 10',embed=embed)
        await asyncio.sleep(540) #wait 9 minutes

        embed2 = discord.Embed( #second embed for second ping
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

#help function
@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = 'Help',
    description = '씨바-bot Help Library. These are the following commands everyone can use in this server currently. (The prefix to use commands is ";") Note that the commands are case-sensitive.',
    colour = discord.Colour.purple()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_image(url=siba_img_landscape)
  embed.set_author(name='씨바-bot')

  embed.add_field(name='General Commands',value='\u200b', inline=False)
  embed.add_field(name=';sale [meso amount] [party size] [mvp status]',value='Calculate sale given initial amount, number of members, and mvp status e.g ;sale 1800000000 4 1', inline=True)
  embed.add_field(name=';checklist',value='View the pre-run checklist that you should go through prior to runs', inline=True)

  embed.add_field(name='씨바-Server Commands',value='\u200b', inline=False)
  embed.add_field(name=';logo [number]',value='View company logo', inline=True)
  embed.add_field(name=';schedule',value='View reminder for boss runs and GPQ', inline=True)
  embed.add_field(name=';parties',value='View all the parties along with each runner', inline=True)
  embed.add_field(name=';ping',value='Weekly boss run ping (Party Leaders Only)', inline=True)
  await ctx.send(embed=embed)

#calculate sale
@client.command()
async def sale(ctx,capital=1,pty=1,mvp=0):
  try:
    tax = 0.03 if mvp else 0.05
    amt = math.floor(capital * (1-  tax) / (pty - 0.05))
    await ctx.send(f'{amt:,} meso(s) each')
  except ValueError:
    await ctx.send('Invalid parameters used. (Type ;help for more information)')

#display runners
@client.command()
async def parties(ctx):
  embed = discord.Embed(
    title = 'Runners',
    description = 'Below are the following parties a long with each member',
    colour = discord.Colour.red()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://static.wikia.nocookie.net/maplestory/images/6/68/Mob_Will_%283%29.png/revision/latest?cb=20180127074010')
  embed.set_author(name='씨바-bot')
  embed.add_field(name='Chilly Line',value = 'Chilly, Eric, Harry, AJ',inline=True)
  embed.add_field(name='Dan Line',value = 'Dan, Yena, Seb, Jay',inline=True)
  embed.add_field(name='Kevin Line',value = 'Kevin :skull:',inline=True) 
  await ctx.send(embed=embed)

#display prerun checklist
@client.command()
async def checklist(ctx):
  embed = discord.Embed(
    title = 'Pre-run Checklist',
    description = 'Make sure everything is set and ready to go, prior to the boss runs.',
    colour = discord.Colour.blue()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/thin-line-color-2/21/27-512.png')
  embed.add_field(name='Please check the following items:',value='<:verified:847677650750144542> Legion setup\n<:verified:847677650750144542> Link skills\n<:verified:847677650750144542> Hyper skills\n<:verified:847677650750144542> Hyper stats\n<:verified:847677650750144542> Buff freezers\n<:verified:847677650750144542> Familiars\n<:verified:847677650750144542> Check pets/pet food\n<:verified:847677650750144542> Bossing equips/rings',inline=False)
  embed.add_field(name='Also, check these additional items:',value='\n<:verified:847677650750144542> Green bind \n<:verified:847677650750144542> Nodes\n<:verified:847677650750144542> Links\n<:verified:847677650750144542> Legion\n<:verified:847677650750144542> Monster park extreme potions\n<:verified:847677650750144542> Guild skills\n<:verified:847677650750144542> Guild blessing\n<:verified:847677650750144542> Ursus\n<:verified:847677650750144542> Cold winter/HT/apple/tengu buffs\n<:verified:847677650750144542> Candied apples\n<:verified:847677650750144542> Level 250/275 Fame buff\n<:verified:847677650750144542> Boss rush pots\n<:verified:847677650750144542> Alchemy stat potion I - X\n<:verified:847677650750144542> MVP superpower\n<:verified:847677650750144542> Echo\n<:verified:847677650750144542> Familiars setup\n<:verified:847677650750144542> Weapon tempering',inline=False)
  await ctx.send(embed=embed)


#display schedules
@client.command()
async def schedule(ctx):
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

#reminder boss run ping
@client.command(name='ping')
@commands.has_any_role('Developer','Board of Directors','administrator')
async def ping_party(ctx):

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


#====Other Random Commands====#

#logo
@client.command()
async def logo(ctx,logo=1):
  embed = discord.Embed(
    colour = discord.Colour.purple()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_image(url=siba_img_landscape)
  await ctx.send(embed=embed)

#check message
@client.event
async def on_message(message):
  if message.author != client.user: #if not the bot
    if message.content.lower() in ['gary','yena','sus']:
      await message.channel.send('sus')
    if message.content.lower() in ['kevin','kev']:
      await message.channel.send('<:kevin:845474836271595530>')
    if message.content.lower() in ['ssibal','sibal']:
      await message.channel.send('noma')
    if message.content in ['<:Wall:818644951012474901>']:
      await message.channel.send('<:Wall:818644951012474901>')
    await client.process_commands(message)


@client.command()
async def test_embed(ctx): #test f-string for flag race ping
  embed = discord.Embed(
    title = 'Test'
  )
  channel = client.get_channel(845758630263259146)
  role = get(channel.guild.roles, name = 'Developer')
  await channel.send(f'{role.mention} in 1',embed=embed)
  

keep_alive() #using uptimerobot.com
client.run(os.environ['token'])