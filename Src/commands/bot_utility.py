import discord
from discord import app_commands
import blacklist
from config import MOD_ROLE_ID, ADMIN_ROLE_ID
from utility import is_jailed


def setup(tree: app_commands.CommandTree, client: discord.Client) -> None:
    @tree.command(name="ping", description="Replies with pong")
    async def ping(interaction: discord.Interaction) -> None:
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        if blacklist.is_blacklisted(interaction.user.id):
            await interaction.response.send_message("You are blacklisted!")
            return
        elif is_jailed(interaction):
            await interaction.response.send_message("You are in jail!")
            return

        latency = round(client.latency * 1000)

        await interaction.response.send_message(f"Pong!\ntook `{latency}ms`")

    @tree.command(name="dm", description="Send a DM to a user (Staff only)")
    async def dm_user(
        interaction: discord.Interaction,
        user: discord.Member,
        message: str,
        reason: str = "No reason provided",
    ) -> None:
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        # Permission check: only mods and admins
        if not any(
            role.id in (MOD_ROLE_ID, ADMIN_ROLE_ID) for role in interaction.user.roles
        ):
            await interaction.response.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
            return

        # Check if the command user is blacklisted or jailed
        if blacklist.is_blacklisted(interaction.user.id):
            await interaction.response.send_message(
                "You are blacklisted!", ephemeral=True
            )
            return
        elif is_jailed(interaction):
            await interaction.response.send_message("You are in jail!", ephemeral=True)
            return

        embed = discord.Embed(
            title="Hello, message from Ruxy!!",
            description=message,
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text="DO NOT REPLY TO THIS DM")

        try:
            await user.send(embed=embed)
            await interaction.response.send_message(
                f"DM sent successfully to {user.mention}."
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                f"Cannot DM {user.mention}. Their DMs are disabled.",
                ephemeral=True,
            )
        except Exception as error:
            await interaction.response.send_message(
                f"Unexpected error :- {error} \n\n**Contact support team!**"
            )
