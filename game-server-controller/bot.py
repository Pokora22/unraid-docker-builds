import os
import subprocess
import discord

GUILD_ID  = int(os.environ["DISCORD_GUILD_ID"])
TOKEN     = os.environ["DISCORD_TOKEN"]
CONTAINER = "Soulmask"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def run_docker(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def is_running():
    _, out, _ = run_docker("docker", "ps", "-q", "-f", f"name={CONTAINER}")
    return bool(out)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    if not msg.guild or msg.guild.id != GUILD_ID:
        return

    cmd = msg.content.strip().lower()

    if cmd == "!start":
        if is_running():
            await msg.reply(f"`{CONTAINER}` is already running.")
            return
        code, _, err = run_docker("docker", "start", CONTAINER)
        await msg.reply(f"Started `{CONTAINER}`." if code == 0 else f"Failed: `{err}`")

    elif cmd == "!stop":
        if not is_running():
            await msg.reply(f"`{CONTAINER}` is not running.")
            return
        code, _, err = run_docker("docker", "stop", CONTAINER)
        await msg.reply(f"Stopped `{CONTAINER}`." if code == 0 else f"Failed: `{err}`")

    elif cmd == "!restart":
        if not is_running():
            await msg.reply(f"`{CONTAINER}` is not running, not restarting.")
            return
        code, _, err = run_docker("docker", "restart", CONTAINER)
        await msg.reply(f"Restarted `{CONTAINER}`." if code == 0 else f"Failed: `{err}`")


client.run(TOKEN)
