from split_strings import *


async def create_table(text, con, coms):
    name = split_table(text.content).lower()
    try:
        con.execute('CREATE TABLE "%s" (author text, message text, serverId text,word text)' % name)
        con.execute('INSERT INTO "Category" VALUES ("**%s**","%s")' % (name, text.guild.id))
    except:
        print("Table already created")
    else:
        await coms('Created table: %s' % name)
        con.commit()


async def add_word(msg, con, coms, server):
    args = split_table_name(msg)
    print(args)
    word = args[0]
    table_name = args[1]
    try:
        con.execute(f'SELECT * FROM {table_name}')
    except:
        await coms(f"Category {table_name} doesn't exist")
    else:
        try:
            con.execute(f'INSERT INTO "Words" VALUES ("%s", "%s", "%s")' % (word, server, table_name.lower()))
        except:
            await coms(f"{word} is already categorized")
        else:
            await coms('Added %s to %s' % (word, table_name))
            con.commit()


async def print_category(msg, con, coms, server):
    name = split_table_name(msg)[1]
    try:
        result = con.execute(f'SELECT COUNT(*) FROM {name} WHERE serverId = {server}')
    except:
        await coms(f"Category {name} doesn't exist")
        return
    else:
        for i in result:
            if i[0] == 0:
                await coms(f'''Category {name} is empty(no specific word belonging to the category was said or server specific category)''')
                return
    try:
        rows = con.execute(f"SELECT author, message, word FROM {name} WHERE serverId = {server}")
    except:
        await coms(f"{name} isn't a Category")
    else:
        for row in rows:
            await coms(f'**{row[0]}** said: {row[1]}, with key word: **{row[2]}**')

async def print_all(con, coms, server):
    try:
        result = con.execute(f'SELECT COUNT(*) FROM Category WHERE serverId = {server}')
    except:
        print("Error")
    else:
        for i in result:
            if i[0] == 0:
                await coms(f"There is no Categories yet in this Server")
                return
    try:
        rows = con.execute(f'SELECT cat, serverId FROM Category WHERE serverId = {server}')
    except:
        print("Error")
    else:
        result = ""
        for row in rows:
            result += f"{row[0]} "
        await coms(result)