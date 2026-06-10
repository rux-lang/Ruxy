import discord
from discord import app_commands
import os
import sys
from utility import is_allowed

from config import OWNERS


def setup(tree: app_commands.CommandTree, client: discord.Client) -> None:
    @tree.command(name="shutdown", description="Shuts down the bot")
    async def shutdown(interaction: discord.Interaction) -> None:
        if not is_allowed(interaction, [], OWNERS):
            await interaction.response.send_message(
                "You cannot use this command.", ephemeral=True
            )
            return

        await interaction.response.send_message("Shutting down...", ephemeral=True)

        await client.close()

    @tree.command(name="restart", description="Restarts Ruxy")
    async def restart(interaction: discord.Interaction) -> None:
        if not is_allowed(interaction, [], OWNERS):
            await interaction.response.send_message(
                "You cannot use this command.", ephemeral=True
            )
            return

        await interaction.response.send_message("Restarting...", ephemeral=True)

        os.execv(sys.executable, [sys.executable] + sys.argv)  # nosec
