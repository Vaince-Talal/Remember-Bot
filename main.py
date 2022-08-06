import discord
import sqlite3
from split_strings import *
client = discord.Client()

wordID = 0
databaseName = 'test6'
con = sqlite3.connect(databaseName+'.db')
commands = ['$create table - creates a table with a name corresponding to the category ', "$print tableName - prints the corresponding table","$add word tableName - adds a word for the bot to watch for and adds it to "]


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
        args = con.execute(f'SELECT * FROM "Servers" WHERE serverName="{guild.name}"')
        for arg in args:
            if len(arg) == 0:
                con.execute(f'INSERT INTO "Servers" VALUES("{guild.name}", "{guild.id}")')
        print(f'Guilds: {guild.name}')
        con.commit()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    coms = message.channel.send
    server = str(message.guild.id)

    if message.author == client.user:
        return

    if msg.startswith('$help'):
        for i in commands:
            await coms(f"{i}")



        #print("No words currently")

    if msg.startswith("$create table"):
        name = split_table(msg).lower()
        try:
            con.execute('CREATE TABLE "%s" (author text, message text, serverId int,cat text)' % name)
            con.execute('INSERT INTO "Category" VALUES ("**%s**","%s","%s")' % (name, message.guild.name, message.guild.id))
        except:
            print("Table already created")
        else:
            await coms('Created table: %s' % name)
            con.commit()

    if msg.startswith("$add "):
        args = split_table_name(msg)
        print(args)
        word = args[0]
        table_name = args[1]
        try:
            con.execute(f'SELECT * FROM {table_name}')

        except:
            await coms(f"{table_name} doesn't exist")
        else:
            try:
                con.execute(f'INSERT INTO "Words" VALUES ("%s", "%s", "%s")' % (word, server, table_name))
            except:
                await coms(f"{word} is already catergorized")
            else:
                await coms('Added %s to %s' % (word, table_name))
        con.commit()

    if msg.startswith("$print table"):
        name = split_table_name(msg)
        rows = con.execute(f'SELECT * FROM {name[1]}')
        for row in rows:
            result = ""
            for i in range(0,len(row)-1):
                result += f"{row[i]}, "
            result += f"{row[i+1]}"
            await coms(result)

    rows = con.execute('SELECT word, cat FROM Words')
    for row in rows:
        print(len(row))
        print(row[0])
        if row[0] in msg:
            await coms("%s from: %s has been recorded into the database belonging to %s category" % (message.content, message.author, row[1]))
            con.execute(f'INSERT INTO "{row[1].lower()}" VALUES ()')

@client.event
async def on_guild_join(guild):
    con.execute('INSERT INTO "Servers" VALUES ("%s","%s")' % (guild.name, guild.id))
    con.commit()




client.run('MTAwMjA2MjI5OTY0MjcyODUzOQ.G-hu-4.WDeHqc_ilwlU34pTP0e0QlU5eQL-fP8vtHeovg')
