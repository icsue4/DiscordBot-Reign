import discord
from discord.ext import commands
import string
from paramiko import SSHClient

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is alive. Yay')
    print(f'Logged on as {bot.user}!')
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("That Waffle"))

@bot.hybrid_command()
async def sync(ctx: commands.Context):
    await ctx.send("Syncing...")
    await bot.tree.sync()

@bot.hybrid_command()
async def clear(ctx: commands.Context):
    await ctx.channel.purge()

@bot.hybrid_command()
async def info(ctx: commands.Context):
    await ctx.send("Info:")
    await ctx.send(ctx.author)
    await ctx.send(ctx.guild)

# Runs a Rotx cipher
@bot.hybrid_command()
async def rot(ctx: commands.Context, arg1, arg2):
    alphabet = string.ascii_lowercase
    x = ''.join([alphabet[(alphabet.find(letter) + int(arg2)) % 26] if alphabet.find(letter) >= 0 else letter for letter in arg1.lower()])
    await ctx.send(f"Rot{arg2} Results: Plain Text [{arg1}] | Cipher Text [{x}]")

# Checks hostname with single user ssh login
@bot.hybrid_command()
async def ssh(ctx, ip, user_name, user_pass):
    client = SSHClient()
    client.load_system_host_keys()
    try:
        client.connect(hostname=ip, username=user_name, password=user_pass)
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("whoami")
        output1 = ssh_stdout.readline().strip()
        await ctx.send(f"{output1}")
        client.close()
    except Exception as error_message:
        await ctx.send("Unable to connect | Connection FAIL")
        await ctx.send(error_message)
    try:
        client.connect(hostname=ip, username=user_name, password=user_pass)
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("hostname")
        output2 = ssh_stdout.readline().strip()
        await ctx.send(f"{output2}")
        client.close()
    except Exception as error_message:
        await ctx.send("Unable to connect | Connection FAIL")
        await ctx.send(error_message)

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(1298101145985617993)
    print(f"{member} joined the guild!")
    await welcome_channel.send(f"{member.mention}, Welcome to the Guild!")

@bot.event   
async def on_message(message):
    print(f'Message from {message.guild}|{message.author}: {message.content}')
    if(message.content == "bitchin"):
        spitout = (22 + 24 - 3)
        await message.reply(f"No, {message.author}, you are bitchin. And the answer is {spitout}!")
    elif(message.content == "!ping"):
        print("This worked! PONG")
        await message.reply("Pong!")
    elif(message.content == "!rot13"):
        x = message.content
        await message.reply(f"cipher text | {x}")




























bot.run("")