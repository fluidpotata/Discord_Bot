import discord
import requests


async def wait(ctx):
    msg = await ctx.send("Hang in there....")
    return msg


async def memjoined(member):
    channel = member.guild.system_channel

    await channel.send(
        f"Welcome, {member.mention}! We're excited to have you here! Please check the #rules channel! Thanks!"
    )


async def reactloading(message):
    await message.add_reaction('ADd reaction id here')


async def removeloading(message, user):
    await message.remove_reaction('ADd reaction id here', user)


async def reactdone(message):
    await message.add_reaction('ADd reaction id here')


async def reacterror(message):
    await message.add_reaction('ADd reaction id here')


async def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    joke_data = response.json()

    if response.status_code != 200:
        return ("Failed to fetch joke")

    joke = f"{joke_data['setup']} {joke_data['punchline']}"
    return joke


# def final(data):
#     try:
#         connection = mysql.connector.connect(host=os.environ['host'],
#                                              user=os.environ['username'],
#                                              password=os.environ['password'],
#                                              database=os.environ['database'],
#                                              port=os.environ['port'])
#         cursor = connection.cursor()
#         cursor.execute(
#             f"select * from final_f23 where course = '{data[0]}' and section = '{data[1]}';"
#         )
#         out = cursor.fetchall()
#         out = out[0]
#         result = f"""```Course: {out[0]}\nSection: {out[1]}\nDate: {out[2]}\nTime: {out[3]}-{out[4]}\nRoom: {out[5]}\nMode: {out[6]}```\n"""
#         cursor.close()
#         connection.close()
#         return result
#     except:
#         return "Database busy! Try again after 5mins!"
