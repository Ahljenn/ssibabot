import discord
import locale
import os
import math
import datetime
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from keep_alive import keep_alive #import method from py file

client = commands.Bot(command_prefix = ';') #prefix
locale.setlocale(locale.LC_ALL, '') # for comma separation

siba_img = 'https://cdn.discordapp.com/attachments/838627115326636082/845048535023747102/image0.jpg'
siba_img_landscape = 'https://cdn.discordapp.com/attachments/836716455072235541/845093553821581363/siba.jpg'
company_logos =[siba_img,siba_img_landscape]

#get guild channel id
async def scheduled_function(): 
  c = client.get_channel(838627115326636082)
  await c.send('TEST0')

#when run
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you sleep | ;commands'))
    scheduler = AsyncIOScheduler()

    #run from monday-sunday 4am, 11am, 1pm, 2pm, 3pm
    now = datetime.datetime.now(timezone('US/Pacific'))
    print(now)
    scheduler.add_job(scheduled_function, 'cron', day_of_week='mon-sun', hour=22, minute = 51)


    scheduler.start()
    print('Bot is deployed...')

#flag race reminder
#initialize task
#get time NOW

#while True
#(if time is 4am PDT || 11AM || 1PM || 2PM || 3PM == time NOW: -   send unique embed for each time
#then send ping 


#Help
@client.command()
async def commands(ctx):
  embed = discord.Embed(
    title = 'Help',
    description = '씨바-bot Help Library. These are the following commands everyone can use in this server currently. (The prefix to use commands is ";")',
    colour = discord.Colour.purple()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_image(url=siba_img_landscape)
  embed.set_author(name='씨바-bot')

  embed.add_field(name='General Commands',value='\u200b', inline=False)
  embed.add_field(name=';sale [meso amount] [party size] [mvp status]',value='Calculate sale given initial amount, number of members, and mvp status e.g ;sale 1800000000 4 1', inline=True)
  embed.add_field(name=';reset',value='(Disabled currently) Calculate time until now and reset time', inline=False)
  embed.add_field(name=';logo [number]',value='View company logo', inline=True)
  embed.add_field(name=';reminder',value='View reminder for boss runs and GPQ', inline=True)

  embed.add_field(name='Party Commands',value='\u200b', inline=False)
  embed.add_field(name=';party1',value='Display party1 (Chilly line)', inline=True)
  embed.add_field(name=';party2',value='Display party2 (Dan line)', inline=True)
  embed.add_field(name=';party3',value='Display party3 (Kevin line)', inline=True)
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

#Party 1 (Chilly) Line
@client.command()
async def party1(ctx):
  embed = discord.Embed(
    title = 'Chilly Line',
    description = 'Members of Chilly line',
    colour = discord.Colour.purple()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url=siba_img)
  embed.set_author(name='씨바-bot')
  embed.add_field(name='Member 1: [Leader]',value='Chilly', inline=False)
  embed.add_field(name='Member 2:',value='Eric', inline=True)
  embed.add_field(name='Member 3:',value='Harry', inline=True)
  embed.add_field(name='Member 4:',value='AJ', inline=True)
  await ctx.send(embed=embed)

#Party 2 (Chilly) Line
@client.command()
async def party2(ctx):
  embed = discord.Embed(
    title = 'Dan Line',
    description = 'Members of Dan line',
    colour = discord.Colour.purple()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url=siba_img)
  embed.set_author(name='씨바-bot')
  embed.add_field(name='Member 1: [Leader]',value='Dan', inline=False)
  embed.add_field(name='Member 2:',value='Jay', inline=True)
  embed.add_field(name='Member 3:',value='Yena', inline=True)
  embed.add_field(name='Member 4:',value='Seb', inline=True)
  await ctx.send(embed=embed)

#Party 3 Kevin
@client.command()
async def party3(ctx):
  embed = discord.Embed(
    title = 'Kevin Line',
    description = 'Member(s) of Kevin line',
    colour = discord.Colour.purple()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url=siba_img)
  embed.set_author(name='씨바-bot')
  embed.add_field(name='Member 1: ',value='Kevin', inline=False)
  await ctx.send(embed=embed)

#embed party 1/2 schedules
@client.command()
async def reminder(ctx):
  embed = discord.Embed(
    title = 'Schedule Reminder',
    description = 'Below is the usual times Chilly line and Dan line will run.',
    colour = discord.Colour.blue()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://students.wustl.edu/wp-content/uploads/2018/08/Schedule.png')
  embed.set_author(name='씨바-bot')
  embed.add_field(name='Boss Runs [Saturday]: ',value='8:30PM (PST) | 11:30 PM (EST) | 1:30 PM (AEST)', inline=False)
  embed.add_field(name='GPQ [Sunday]: ',value='7:00PM (PST) | 10:00 PM (EST) | 12:00 PM (AEST)', inline=False)
  await ctx.send(embed=embed)

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

# @client.command()
# async def logo2(ctx):
#   embed = discord.Embed(
#     colour = discord.Colour.purple()
#   )
#   embed.set_footer(text='Powered by 씨발')
#   embed.set_image(url=siba_img_landscape)
#   await ctx.send(embed=embed)


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