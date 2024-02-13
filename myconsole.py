from time import time, ctime
from resources import connectDB


async def log(bot, cmd, auth):
    txt =(f"{cmd} was used by {auth} at {ctime(time())}\n")
    connection = connectDB
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO logss values('{txt}')")
    cursor.close()
    connection.close()


async def ready(bot):
    txt = f"Bot started at {ctime(time())}\n"
    connection = connectDB
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO logss values('{txt}')")
    cursor.close()
    connection.close()

# Used the below function to keep the bot running before hosting on Microsoft Azure
# async def running(bot):
#     txt = f"Bot is still running!\n"
#     x = bot.get_channel("A discord Channel!")
#     await x.send(txt)