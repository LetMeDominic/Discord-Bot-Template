from typing import AsyncContextManager
import discord
import os
import random
from discord import message
from discord import guild
from discord import permissions
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import guild_only


client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Helping Shakrs Server'))

@client.command()
async def clear(ctx, ammount=5):
    await ctx.channel.purge(limit=ammount)



@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@client.command()
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    mbed = discord.Embed(
        title = 'Success!',
        description = f"{user} has been successfully unbanned"
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed=mbed)
        await guild.unban(user=user)



@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send( ctx.channel.mention + " has been locked")    


@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send( ctx.channel.mention + " has been unlocked")


@client.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode to delay in this channel to {seconds} seconds!")


@client.command(pass_content=True)
async def changenick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


@client.command()
async def poll(ctx, *,message):
    emb=discord.Embed(title=" POLL ", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@client.command()
async def massunban(ctx):
    banlist = await ctx.guild.bans()
    for users in banlist:
        try:
            await ctx.guild.unban(user=users.user)
        except:
            pass
    await ctx.send("Mass unbanning")


@client.command()
async def mute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="Muted", permissions=perms)
        await  member.add_roles(role)
        await ctx.send(f"{member} has been muted")
    else:
        await member.add_roles(role)
        await ctx.send(f"{member} has been muted")


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certian.',
                'Without a doubt',
                'Yes definitely',
                'Yes',
                'No',
                'Do not count on it',
                'My sources say no']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')



@client.event
async def on_ready():
    print('Bot is online')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.lunoad_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run('Token')
