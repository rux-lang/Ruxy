import discord
import blacklist
from utility import is_jailed

def setup(tree, client):
    @tree.command(
        name="ping",
        description="Replies with pong"
    )
    async def ping(interaction: discord.Interaction):
        if (blacklist.is_blacklisted(interaction.user.id)):
            await interaction.response.send_message("You are blacklisted")
            return
        elif (is_jailed(interaction)):
            await interaction.response.send_message("You are in jail")
            return

        latency = round(client.latency * 1000)

        await interaction.response.send_message(
            f"Pong!\n"
            f"took `{latency}ms`"
        )