import asyncio
import os
import discord
from discord import app_commands

GUILD_ID   = int(os.environ["DISCORD_GUILD_ID"])
TOKEN      = os.environ["DISCORD_TOKEN"]
CONTAINERS = [c.strip() for c in os.environ["CONTAINERS"].split(",")]

intents = discord.Intents.default()
client  = discord.Client(intents=intents)
tree    = app_commands.CommandTree(client)
guild   = discord.Object(id=GUILD_ID)


async def run_docker(*args):
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode().strip(), stderr.decode().strip()


async def is_running(container: str) -> bool:
    _, out, _ = await run_docker("docker", "ps", "-q", "-f", f"name=^{container}$")
    return bool(out)


async def container_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=c, value=c)
        for c in CONTAINERS if current.lower() in c.lower()
    ]


def unknown_container_msg(container: str) -> str:
    return f"`{container}` is not in the allowed container list."


@tree.command(name="start", description="Start a container", guild=guild)
@app_commands.autocomplete(container=container_autocomplete)
async def start_cmd(interaction: discord.Interaction, container: str):
    if container not in CONTAINERS:
        await interaction.response.send_message(unknown_container_msg(container), ephemeral=True)
        return
    await interaction.response.defer()
    if await is_running(container):
        await interaction.followup.send(f"`{container}` is already running.")
        return
    code, _, err = await run_docker("docker", "start", container)
    await interaction.followup.send(
        f"Started `{container}`." if code == 0 else f"Failed to start `{container}`: `{err}`"
    )


@tree.command(name="stop", description="Stop a container", guild=guild)
@app_commands.autocomplete(container=container_autocomplete)
async def stop_cmd(interaction: discord.Interaction, container: str):
    if container not in CONTAINERS:
        await interaction.response.send_message(unknown_container_msg(container), ephemeral=True)
        return
    await interaction.response.defer()
    if not await is_running(container):
        await interaction.followup.send(f"`{container}` is not running.")
        return
    code, _, err = await run_docker("docker", "stop", container)
    await interaction.followup.send(
        f"Stopped `{container}`." if code == 0 else f"Failed to stop `{container}`: `{err}`"
    )


@tree.command(name="restart", description="Restart a container", guild=guild)
@app_commands.autocomplete(container=container_autocomplete)
async def restart_cmd(interaction: discord.Interaction, container: str):
    if container not in CONTAINERS:
        await interaction.response.send_message(unknown_container_msg(container), ephemeral=True)
        return
    await interaction.response.defer()
    if not await is_running(container):
        await interaction.followup.send(f"`{container}` is not running, not restarting.")
        return
    code, _, err = await run_docker("docker", "restart", container)
    await interaction.followup.send(
        f"Restarted `{container}`." if code == 0 else f"Failed to restart `{container}`: `{err}`"
    )


@client.event
async def on_ready():
    await tree.sync(guild=guild)
    print(f"Logged in as {client.user}, synced slash commands to guild {GUILD_ID}")


client.run(TOKEN)
