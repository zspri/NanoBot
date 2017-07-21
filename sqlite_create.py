import sqlite3
import discord
import asyncio

client = discord.Client()

connection = sqlite3.connect("bot.db")
cursor = connection.cursor()

try:
    cursor.execute("DROP TABLE bot;")
except:
    pass

@client.event
async def on_ready():
    cursor.execute("""
    CREATE TABLE bot (
    server_id VARCHAR(30),
    autorole int(0),
    );""")
    connection.commit()
    for server in client.servers:
        cursor.execute("""INSERT INTO bot (server_id, autorole)
        VALUES ({}, 0)""".format(str(server.id)))
