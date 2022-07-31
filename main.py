import discord
import sqlite3
from split_strings import *
client = discord.Client()

databaseName = 'asdf'
con = sqlite3.connect(databaseName+'.db')
commands = ['$create table - creates a table with a name corresponding to the caterogry ', "$print table - prints the corresponding table"]
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'Guilds: {guild.name}')
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    server = message.guild.name
    msg = message.content
    coms = message.channel.send
    if message.author == client.user:
        return
    if msg.startswith('$help'):
        for i in commands:
            await coms(f"{i}")

    if 'mani' in msg:
        con.execute("INSERT INTO LOG VALUES ('**%s**','%s')" % (message.author, message.content))
        await message.channel.send('%s' % message.author.mention)
        con.commit()

    if msg.startswith("$create table"):
        name = split_table(msg)
        con.execute(f'CREATE TABLE "%s" (author text, message text)' % (server + '-' + name))
        con.execute('CREATE TABLE "%s"(word text, id int)' % (server+'-' + name + '-words'))
        await message.channel.send(f'Created table: %s' % (name))
        con.commit()
    if msg.startswith("$add "):
        args = split_table_name(msg)
        word = args[0]
        table_name = args[1]

    if msg.startswith("$print table"):
        name = split_table_name(msg)
        for row in con.execute('SELECT * FROM LOG'):
            await message.channel.send(f'{row[0]} said: {row[1]}')

client.run('MTAwMjA2MjI5OTY0MjcyODUzOQ.G-hu-4.WDeHqc_ilwlU34pTP0e0QlU5eQL-fP8vtHeovg')
