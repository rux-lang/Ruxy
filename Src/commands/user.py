import discord
from discord import app_commands
import blacklist
from utility import is_jailed


def setup(tree: app_commands.CommandTree, client: discord.Client) -> None:
    @tree.command(name="whoami", description="Information about you")
    async def whoami(interaction: discord.Interaction) -> None:
        if blacklist.is_blacklisted(interaction.user.id):
            await interaction.response.send_message("You are blacklisted")
            return
        elif is_jailed(interaction):
            await interaction.response.send_message("You are in jail")
            return

        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        user = interaction.user

        color = (
            user.top_role.color
            if hasattr(user, "top_role")
            else discord.Color.blurple()
        )

        embed = discord.Embed(title="Who Am I?", color=color)

        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="Display Name", value=user.display_name, inline=False)
        embed.add_field(
            name="Account Creation",
            value=user.created_at.strftime("%d %b %Y"),
            inline=False,
        )
        embed.add_field(name="ID", value=user.id, inline=False)

        nickname = user.nick if hasattr(user, "nick") else None
        embed.add_field(name="Nickname", value=nickname or "None", inline=False)

        joined_at = user.joined_at if hasattr(user, "joined_at") else None

        embed.add_field(
            name="Server Join",
            value=(joined_at.strftime("%d %b %Y") if joined_at else "Unknown"),
            inline=False,
        )

        roles_list = user.roles if hasattr(user, "roles") else []

        embed.add_field(
            name="Roles",
            value=", ".join(
                role.name for role in roles_list if role.name != "@everyone"
            )
            or "None",
            inline=False,
        )

        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

    @tree.command(name="whois", description="Shows information about a user")
    async def whois(interaction: discord.Interaction, user: discord.Member) -> None:
        if blacklist.is_blacklisted(interaction.user.id):
            await interaction.response.send_message("You are blacklisted")
            return
        elif is_jailed(interaction):
            await interaction.response.send_message("You are in jail")
            return

        embed = discord.Embed(
            title=f"{user.display_name}'s Profile", color=user.top_role.color
        )

        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="Display Name", value=user.display_name, inline=False)
        embed.add_field(
            name="Account Creation",
            value=user.created_at.strftime("%d %b %Y"),
            inline=False,
        )
        embed.add_field(name="ID", value=str(user.id), inline=False)
        embed.add_field(name="Nickname", value=user.nick or "None", inline=False)

        embed.add_field(
            name="Server Join",
            value=(
                user.joined_at.strftime("%d %b %Y") if user.joined_at else "Unknown"
            ),
            inline=False,
        )

        embed.add_field(
            name="Roles",
            value=", ".join(
                role.name for role in user.roles if role.name != "@everyone"
            )
            or "None",
            inline=False,
        )

        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed)
