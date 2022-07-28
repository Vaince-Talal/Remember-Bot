import discord
import sqlite3
from SQLDatabase import *
client = discord.Client()

databaseName = 'asdf'
con = sqlite3.connect(databaseName+'.db')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return

    if message.content.startswith('mani'):
        con.execute("INSERT INTO LOG VALUES ('%s','%s')" % (message.author, message.content))
        await message.channel.send('%s' % message.author.mention)
        con.commit()

    if message.content.startswith("$create table"):
        con.execute('CREATE TABLE LOG (author text, message text)')
        await message.channel.send(f'{message.author.mention} it works broski')
        con.commit()

client.run('MTAwMjA2MjI5OTY0MjcyODUzOQ.G-hu-4.WDeHqc_ilwlU34pTP0e0QlU5eQL-fP8vtHeovg')
