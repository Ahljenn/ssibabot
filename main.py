import discord
import random
import locale
import os
import math
from discord.ext import commands

client = commands.Bot(command_prefix = ';') #prefix
locale.setlocale(locale.LC_ALL, '') # for comma separation

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you sleep'))
    print('Bot is deployed...')

#calculate sale
@client.command(aliases=['sale'])
async def _sale(ctx,capital=1,pty=1,mvp=0):
    tax = 0.03 if mvp else 0.05
    amt = math.floor(capital * (1-  tax) / (pty - 0.05))
    await ctx.send(f'{amt:,} meso(s) each')

#Help
@client.command()
async def commands(ctx):
  embed = discord.Embed(
    title = 'Help',
    description = '씨바-bot Help Library. The prefix to use these bot commands is currently ";"',
    colour = discord.Colour.blue()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://scontent-sjc3-1.xx.fbcdn.net/v/t31.18172-8/24172987_312331502617128_2923852705315602811_o.jpg?_nc_cat=100&ccb=1-3&_nc_sid=973b4a&_nc_ohc=hBGWzCQGmq0AX-VOup1&_nc_ht=scontent-sjc3-1.xx&oh=f1ddd9641318a6b850a7c7a20ed4dc85&oe=60CD0319')
  embed.set_author(name='씨바-bot')
  embed.add_field(name='sale [meso amount][party size][mvp status]',value='Calculate sale given initial amount, number of members, and mpv status', inline=False)
  embed.add_field(name='party1',value='Display party1 (Chilly line)', inline=False)
  embed.add_field(name='party2',value='Display party2 (Dan line)', inline=False)
  await ctx.send(embed=embed)

#Party 1 (Chilly) Line
@client.command()
async def party1(ctx):
  embed = discord.Embed(
    title = 'Chilly Line',
    description = 'Members of Chilly line',
    colour = discord.Colour.blue()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://scontent-sjc3-1.xx.fbcdn.net/v/t31.18172-8/24172987_312331502617128_2923852705315602811_o.jpg?_nc_cat=100&ccb=1-3&_nc_sid=973b4a&_nc_ohc=hBGWzCQGmq0AX-VOup1&_nc_ht=scontent-sjc3-1.xx&oh=f1ddd9641318a6b850a7c7a20ed4dc85&oe=60CD0319')
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
    colour = discord.Colour.red()
  )
  embed.set_footer(text='Powered by 씨발')
  embed.set_thumbnail(url='https://scontent-sjc3-1.xx.fbcdn.net/v/t31.18172-8/24172987_312331502617128_2923852705315602811_o.jpg?_nc_cat=100&ccb=1-3&_nc_sid=973b4a&_nc_ohc=hBGWzCQGmq0AX-VOup1&_nc_ht=scontent-sjc3-1.xx&oh=f1ddd9641318a6b850a7c7a20ed4dc85&oe=60CD0319')
  embed.set_author(name='씨바-bot')
  embed.add_field(name='Member 1: [Leader]',value='Dan', inline=False)
  embed.add_field(name='Member 2:',value='Jay', inline=True)
  embed.add_field(name='Member 3:',value='Yena', inline=True)
  embed.add_field(name='Member 4:',value='Seb', inline=True)
  await ctx.send(embed=embed)



#embed party 1/2 schedules
client.run(os.environ['token'])