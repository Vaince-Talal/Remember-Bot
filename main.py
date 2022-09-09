import discord
import sqlite3
from commands import *

client = discord.Client()

wordID = 0
databaseName = 'offical'
con = sqlite3.connect(databaseName + '.db')
commands = ['$create table NAME - creates a table with a NAME corresponding to the category ',
            "$print cat TABLE_NAME - prints the corresponding table according to its TABLE_NAME",
            "$add WORD TABLE_NAME - adds a WORD for the bot to watch for and adds it to TABLE_NAME"]
temp = open("key.txt", "r")
key = temp.readline()

@client.event
async def on_ready():
    try:
        con.executescript(f'''
        CREATE TABLE "Words"(word text PRIMARY KEY, serverId text, cat text);
        CREATE TABLE "Servers" (serverName text , serverId text PRIMARY KEY );
        CREATE TABLE "Category" (cat text PRIMARY KEY, serverId text);''')

    except:
        print("Already Created")

    for guild in client.guilds:
        try:
            con.execute(f'INSERT INTO "Servers" VALUES("{guild.name}", "{guild.id}")')
        except:
            print('Already added server')
        else:
            print(f'Added {guild.name}')
            con.commit()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content.lower()
    coms = message.channel.send
    server = str(message.guild.id)

    if message.author == client.user:
        return
    if msg.startswith('$'):
        if msg.startswith('$help'):
            for i in commands:
                await coms(f"{i}")

        if msg.startswith("$create table"):
            await create_table(message, con, coms)

        if msg.startswith("$add "):
            await add_word(msg, con, coms, server)

        if msg.startswith("$print cat"):
            await print_category(msg, con, coms, server)

        if msg.startswith("$print all cats in server"):
            await print_all(con, coms, server)

    else:
        rows = con.execute(f'SELECT word, cat FROM Words WHERE serverId = {server}')
        for row in rows:
            if row[0] in msg:
                await coms("**%s** from: **%s** has been recorded into the database belonging to **%s** category" % (
                message.content, message.author, row[1]))
                con.execute(
                    f'INSERT INTO "{row[1].lower()}" VALUES ("{message.author}", "{message.content}", "{server}", "{row[0]}")')
                con.commit()


@client.event
async def on_guild_join(guild):
    con.execute('INSERT INTO "Servers" VALUES ("%s","%s")' % (guild.name, guild.id))
    con.commit()


client.run(f'{key}')
