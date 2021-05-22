import discord
import locale
import os
import math
import datetime
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive #import method from py file

client = commands.Bot(command_prefix = ';',help_command=None) #prefix
locale.setlocale(locale.LC_ALL, '') # for comma separation

siba_img = 'https://cdn.discordapp.com/attachments/838627115326636082/845048535023747102/image0.jpg'
siba_img_landscape = 'https://cdn.discordapp.com/attachments/836716455072235541/845093553821581363/siba.jpg'
company_logos =[siba_img,siba_img_landscape]
flag_times_pdt = [4,11,13,14,15]
flag_difference = []

# #get guild channel id
# async def scheduled_function(): 
#   c = client.get_channel(838627115326636082)
#   await c.send('TEST0')

# def calculate_time():
#   date_time_now = datetime.datetime.combine(datetime.date.today(), datetime.time(datetime.datetime.now(timezone('US/Pacific')).hour)) #get time now
#   #get time difference related to each flag time
#   for fr_time in flag_times_pdt:
#       date_time_end = datetime.datetime.combine(datetime.date.today(), datetime.time(fr_time)) #get end time 
#       date_difference = date_time_end - date_time_now 
#       diff_hours = date_difference.total_seconds() / 3600
#       flag_difference.append(diff_hours)
#       print(diff_hours)

#when run
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you sleep | ;help'))
    
    # scheduler = AsyncIOScheduler()
    # #get date time
    # calculate_time()
    # #run from monday-sunday 4am, 11am, 1pm, 2pm, 3pm
    # scheduler.add_job(scheduled_function, 'cron', day_of_week='mon-sun', hour=22, minute = 51)
    # scheduler.start()

    print('Bot is deployed...')

#flag race reminder
#initialize task
#get time NOW

#while True
#(if time is 4am PDT || 11AM || 1PM || 2PM || 3PM == time NOW: -   send unique embed for each time
#then send ping 


#Help
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
  embed.add_field(name=';reset',value='(Disabled currently) Calculate time until now and reset time', inline=False)
  embed.add_field(name=';logo [number]',value='View company logo', inline=True)

  embed.add_field(name='Party Commands',value='\u200b', inline=False)
  embed.add_field(name=';schedule',value='View reminder for boss runs and GPQ', inline=True)
  embed.add_field(name=';parties',value='View all the parties along with each runner', inline=True)
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

#calculate time until reset (12AM,Thursday UTC)
@client.command()
async def reset(ctx):
    now = datetime.utcnow()
    d = now
    while d.weekday() != 3:
      d += datetime.timedelta(days=1) #fixme
    elapsed_time = d-now
    divmod(elapsed_time.total_seconds,60)
    await ctx.send(now)

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
  embed.add_field(name='Kevin Line',value = 'Kevin (Traitor)',inline=True) 
  await ctx.send(embed=embed)


#embed party 1/2 schedules
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
  embed.add_field(name='Boss Runs [Saturday]: ',value='8:30PM (PST) | 11:30 PM (EST) | 1:30 PM (AEST)', inline=False)
  embed.add_field(name='GPQ [Sunday]: ',value='7:00PM (PST) | 10:00 PM (EST) | 12:00 PM (AEST)', inline=False)
  await ctx.send(embed=embed)


#reminder boss run ping
@client.command(name='run')
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
  await ctx.send(embed = embed)
  await ctx.send(f"{team1.mention,team2.mention}")


#====Other Random Commands====~
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


#if specific message
@client.event
async def on_message(message):
  if message.author != client.user: #if not the bot
    if message.content.lower() in ['gary','kevin','yena','kev','sus']:
      await message.channel.send('sus')
    if message.content.lower() in ['ssibal','sibal']:
      await message.channel.send('noma')
    await client.process_commands(message)



keep_alive() #using uptimerobot.com
client.run(os.environ['token'])