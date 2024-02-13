import os
import discord
from discord.ext import commands
import myconsole as console
import authenthicate
import response
import resources
import tasks as tk
import asyncio
import requests


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')



@bot.event
async def on_ready():
    print("Bot is ready!")
    await console.ready(bot)
    game = discord.Game("your commands!!")
    await bot.change_presence(status=discord.Status.online, activity=game)
    await bot.tree.sync()

    guilds = [guild async for guild in bot.fetch_guilds(limit=150)]
    print(guilds)



@bot.event
async def on_message(message):
    if authenthicate.ifServer1(message):
        category = message.channel.category
        if int(category.id) not in (1153372075646521384, 1156090385408475257, 1180465508370350080) and category.position != 3:
            await category.edit(position=3)
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    if authenthicate.ifServer1(member):
        await authenthicate.newinServer1(member)
    elif authenthicate.ifServer2(member):
        x = await authenthicate.newinServer2(member)
        alert = bot.get_channel("A channel ID")
        alert_text = await alert.send(
            f"Alert <@&{"A role ID"}>, an intruder joined in <#{x}>"
        )
        if str(member.name)=="A specific username":
            role = member.guild.get_role("A role ID")
            await member.add_roles(role)
            await alert_text.edit(
            content = f"Oh wait nvm"
            )
    else:
        response.memjoined(member)

# @bot.command()
@bot.hybrid_command(name='ping',with_app_command=True)
async def ping(ctx):
    if authenthicate.botstatus() or authenthicate.ifAdmin(ctx):
        await ctx.send("Pong!")
    else:
        await ctx.send("Under maintenance!")
    await console.log(bot,"ping",ctx.author)



@bot.hybrid_command(name='check', description= "Check bot's current status!",with_app_command=True)
async def check(ctx):
    if authenthicate.botstatus():
        embed = discord.Embed(
            title='Bot Status',
            color=discord.Color.green()
        )  
        embed.add_field(name='Status', value='Active', inline=False)        
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Bot Status',
            color=discord.Color.red()
        )
        
        embed.add_field(name='Status', value='Closed', inline=False)       
        await ctx.send(embed=embed)

@bot.command()
async def facinfo(ctx, initial: str = None):
    if authenthicate.botstatus() or authenthicate.ifAdmin(ctx):
        if initial == None:
            await response.reacterror(ctx.message)
            await ctx.send('Put Initial')
        else:
            await response.reactloading(ctx.message)
            ttt = await resources.facultySearch(initial)
            if len(ttt) != 0:
                await response.reactdone(ctx.message)
                await response.removeloading(ctx.message, bot.user)
                for tmp in ttt:
                    await ctx.channel.send(
                        f"""```Name: {tmp[1]}\nInitial: {tmp[0]}\nDesignation: {tmp[2]} \nRoom: {tmp[3]} \nEmail: {tmp[4]}```"""
                    )
            else:
                await response.reacterror(ctx.message)
                await ctx.send(
                    f"No info found. Check if your entry is right.\n- For initial, only use 3 characters \n- For name, use more than 3 characters \n- Faculties outside CSE are hard to find, they are regularly being updated."
                )
    else:
        await ctx.send("Under maintenance!")
    await console.log(bot, f'facinfo for {initial}', ctx.author)


@bot.command()
async def verify(ctx, userID: int):
    user = ctx.guild.get_member(userID)
    if authenthicate.ifAdmin(ctx) :
        await authenthicate.verifymember(ctx, user)
        await response.reactdone(ctx.message)
    await console.log(bot, f'verify for {user.name}', ctx.author)


@bot.command()
async def materials(ctx, code: str):
    if authenthicate.botstatus() or authenthicate.ifAdmin(ctx):
        await response.reactloading(ctx.message)
        msg = await response.wait(ctx)
        stat, output = await resources.materials(ctx, code)
        await response.removeloading(ctx.message, bot.user)
        if stat:
            await response.reactdone(ctx.message)
        else:
            await response.reacterror(ctx.message)
        await msg.edit(content=output)
    else:
        await ctx.send("Under maintenance!")
    await console.log(bot, f'materials', f'ctx.author')

@bot.command()
async def finals(ctx, *data):
    if authenthicate.botstatus():
        await response.reactloading(ctx.message)
        x = [tuple(i.upper().split('-')) for i in data]
        output = ""
        output += f"Routine for <@{ctx.author.id}>\n\n"
        for i in x:
            output += (resources.mid(i))
        await ctx.send(output)
        await response.removeloading(ctx.message, bot.user)
        await response.reactdone(ctx.message)
    else:
        await ctx.send("Under maintenance!")
    await console.log(bot, data, ctx.author)
        

@bot.hybrid_command(name='switch',description="IYKYK", with_app_command=True)
async def botshut(ctx):
    if authenthicate.ifAdmin(ctx):
        authenthicate.tooglebotstatus()
        await ctx.send("Done!")
    else:
        await ctx.send("Not allowed!")




@bot.hybrid_command(name='joke',description="Get random jokes!", with_app_command=True)
async def joke(ctx, num: int = 1):
    await console.log(bot, 'joke', str(ctx.author))
    if num == 1:
        output = await response.get_random_joke()
        await ctx.send(output)
    else:
        for i in range(num):
            output = "- "
            output += await response.get_random_joke()
        await ctx.send(output)


@bot.hybrid_command(name='help',description="Get list of all the available commands!", with_app_command=True)
async def help(ctx):
    await console.log(bot, 'help', str(ctx.author))
    with open("help.txt","r") as f:
        t = ""
        while True:
            tmp = str(f.readline())
            if not tmp:
                break
            t += tmp   
    await ctx.send(t)


@bot.hybrid_command(description="Check tasks!")
async def tasks(ctx):
    y = "Your tasks are:"
    y = tk.data(ctx.author)
    await ctx.send(y)

@bot.hybrid_command(description="Enter task!")
async def enqueue(ctx, taskname):
    if tk.commit(ctx.author, taskname):
        await ctx.send("Done!")


@bot.hybrid_command(description="Remove task!")
async def dequeue(ctx, taskname):
    if tk.rem(ctx.author, taskname):
        await ctx.send("Done!")


@bot.hybrid_command(name='shhh',description="Backup DB!", with_app_command=True)
async def shh(ctx):
    if authenthicate.ifAdmin(ctx):
        await ctx.send(file=discord.File(r'db/bot.db'))
    else:
        await ctx.send("Who r u bradah?")


def bot_run():
    token = "INSERT YOUR TOKEN HERE"
    bot.run(token)

bot_run()