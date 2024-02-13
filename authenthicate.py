import discord


def botstatus():
    """
        Update Idea: Implement with DB
    """
    with open("status.txt") as f:
        return eval(f.readline())


def tooglebotstatus():
    """
        Update Idea: Implement with DB
    """
    if botstatus():
        with open("status.txt", 'w') as f:
            f.writelines("False")
    else:
        with open("status.txt", 'w') as f:
            f.writelines("True")


def ifAdmin(ctx):
    """
        Update Idea: Implement with DB
    """
    if str(ctx.author) == "admin_username":
        return True
    return False


def ifServer1(ctx):
    if int(ctx.guild.id) == int("Server 1 ID"):
        return True
    return False


def ifServer2(ctx):
    if int(ctx.guild.id) == int("Server 2 ID"):
        return True
    return False


async def verifymember(ctx, user):
    role = ctx.guild.get_role("Role ID")
    rrole = ctx.guild.get_role("Removing Role ID")
    await user.add_roles(role)
    await user.remove_roles(rrole)
    overwrites = {
        ctx.guild.default_role:
        discord.PermissionOverwrite(read_messages=False,
                                    send_messages=False,
                                    connect=False,
                                    speak=False)
    }
    category = await ctx.guild.create_category(str(user.name),
                                               overwrites=overwrites)
    channel = await ctx.guild.create_text_channel('text',
                                                  overwrites=overwrites,
                                                  category=category)
    voice = await ctx.guild.create_voice_channel(
        'voice', overwrites=overwrites, category=category)
    await category.set_permissions(user,
                                   read_messages=True,
                                   send_messages=True,
                                   connect=True,
                                   speak=True)
    await channel.send(f"{user.name} is verified!.")


async def newinServer1(member):
    category = discord.utils.get(member.guild.categories,
                                 id="Server 1's category ID")
    channel = await member.guild.create_text_channel(
        f'temp-channel-{member.name}', category=category)
    await channel.set_permissions(member,
                                  read_messages=True,
                                  send_messages=True,
                                  read_message_history=True)
    await channel.send(
        f'Welcome, {member.mention}! Wait for roles. Type **!help** for bot commands.'
    )


async def newinServer2(member):
    category = discord.utils.get(member.guild.categories,
                                 id="Server 2's category ID")
    channel = await member.guild.create_text_channel(f'intruder-{member.name}',
                                                     category=category)
    await channel.set_permissions(member,
                                  read_messages=True,
                                  send_messages=True,
                                  read_message_history=True)
    await channel.send(f'Who are you?! What are you doing here!!!')
    return channel.id
