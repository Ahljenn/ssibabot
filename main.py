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
company_logos =[siba_img,siba_img_landscape]
flag_times_utc = [11,18,20,21,22] #time-1 for 57min

time = datetime.datetime.now

#function timer to send msg at set times
async def timer():
  msg_sent = False

  channel = client.get_channel(838627115326636082)
  flag_role = get(channel.guild.roles, name = 'Developer')

  while not client.is_closed():
    if any(time().hour == flag for flag in flag_times_utc) and time().minute == 50:
      if not msg_sent:
        embed = discord.Embed(
          title = 'Flag Race',
          description = 'Flag race is starting soon in 10 minutes, get ready.',
          colour = discord.Colour.blue(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text='Powered by 씨발')
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Blue_flag_waving.svg/951px-Blue_flag_waving.svg.png')
        embed.set_author(name='씨바-bot')
        await channel.send(f'{flag_role.mention}',embed=embed)
        msg_sent = True
        await asyncio.sleep(60)
      else:
        msg_sent = False
    if any(time().hour == flag for flag in flag_times_utc) and time().minute == 59:
      if not msg_sent:
        embed = discord.Embed(
          title = 'Flag Race',
          description = 'Flag race will be starting soon, get ready.',
          colour = discord.Colour.red(),
          timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text='Powered by 씨발')
        embed.set_thumbnail(url='https://webstockreview.net/images/cone-clipart-triangle-8.png')
        embed.set_author(name='씨바-bot')
        await channel.send(f'{flag_role.mention}',embed=embed)
        msg_sent = True
        await asyncio.sleep(60)
      else:
        msg_sent = False
    await asyncio.sleep(1) 

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you sleep | ;help'))
    client.loop.create_task(timer())
    print('Bot is deployed...')

#display all available functions
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
  embed.add_field(name='Boss Runs [Saturday]: ',value='8:30PM (PST) | 11:30 PM (EST) | 10:30AM (AEST)', inline=False)
  embed.add_field(name='GPQ [Sunday]: ',value='7:00PM (PST) | 10:00 PM (EST) | 11:00AM (AEST)', inline=False)
  await ctx.send(embed=embed)

#reminder boss run ping
@client.command(name='ping')
@commands.has_any_role('Developer','Board of Directors','administrator')
async def ping_party(ctx):

  await schedule(ctx)
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
  try:
    embed.set_footer(text='Powered by 씨발')
    embed.set_image(url=company_logos[logo-1])
    await ctx.send(embed=embed)
  except: #number outside of ValueError
    await ctx.send('Error, there are currently only '+ str(len(company_logos)) + ' company logos to view.')

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
    await client.process_commands(message)

#send lone msg841120354020884480
@client.command()
async def _msg(ctx):
  channel = client.get_channel(841120354020884480)
  await channel.send('yes oppa >< uwu ;; ㅠㅠㅠㅠㅠㅠㅠㅠ')

keep_alive() #using uptimerobot.com
client.run(os.environ['token'])