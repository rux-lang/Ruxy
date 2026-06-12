# SPDX-FileCopyrightText: 2025-present Ahum Maitra theahummaitra@gmail.com
# SPDX-License-Identifier: 	MIT

import random
from datetime import timedelta

import pyjokes
import requests
from discord import Interaction, Member, app_commands

import blacklist
from utility import is_jailed


def setup(tree, client):
    @tree.command(
        name="self-timeout",
        description="Timeout yourself for a specified duration (in minutes)",
    )
    async def self_timeout(interaction: Interaction, duration: int):
        """Allows users to timeout themselves"""

        if duration <= 0:
            await interaction.response.send_message(
                "Invalid request, please enter a valid duration.", ephemeral=True
            )
            return

        if duration > 40320:
            await interaction.response.send_message(
                "You cannot timeout for more than 28 days (40320 minutes).",
                ephemeral=True,
            )
            return

        try:
            await interaction.user.timeout(
                timedelta(minutes=duration),
                reason=f"User-requested timeout for {duration}m",
            )
            await interaction.response.send_message(
                f"Timed out for {duration} minutes."
            )
        except Exception as e:
            await interaction.response.send_message(
                "Failed to apply timeout. Please try again!  **If not working for a long time, contact support team!**",
                ephemeral=True,
            )

    @tree.command(name="joke", description="Get a random joke")
    async def send_joke(interaction: Interaction):
        if blacklist.is_blacklisted(interaction.user.id):
            await interaction.response.send_message("You are blacklisted!")
            return
        elif is_jailed(interaction):
            await interaction.response.send_message("You are in jail!")
            return

        try:
            joke = pyjokes.get_joke()
            await interaction.response.send_message(
                f"**Here's a joke for you:** \n{joke}"
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Failed to fetch a joke. Try again later! **If not working for a long time, contact support team!** \n {e}",
                ephemeral=True,
            )

    @tree.command(name="roast", description="Roast somebody")
    async def do_roast(interaction: Interaction, member: Member) -> None:
        if blacklist.is_blacklisted(interaction.user.id):
            await interaction.response.send_message("You are blacklisted!")
            return
        elif is_jailed(interaction):
            await interaction.response.send_message("You are in jail!")
            return

        try:
            insult = requests.get(
                "https://evilinsult.com/generate_insult.php?lang=en&type=text",
                timeout=5,
            )  # get the insult in plain text
            await interaction.response.send_message(insult.text)
        except Exception as error:
            await interaction.response.send_message(
                f"**Unexpected error, contact support after trying for a while :- ** \n {error}"
            )

    @tree.command(name="rps", description="Play RPS")
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="Rock", value="rock"),
            app_commands.Choice(name="Paper", value="paper"),
            app_commands.Choice(name="Scissors", value="scissors"),
        ]
    )
    async def play_rps(interaction: Interaction, choice: str) -> None:
        if blacklist.is_blacklisted(interaction.user.id):
            await interaction.response.send_message("You are blacklisted!")
            return
        elif is_jailed(interaction):
            await interaction.response.send_message("You are in jail!")
            return

        try:
            computer_choice = random.choice(["rock", "paper", "scissors"])

            if choice == computer_choice:
                await interaction.response.send_message(
                    f"You choose **{choice}**! \n Computer choose: **{computer_choice}**! \n _**It's a draw!**_"
                )
                return
            elif (
                (choice == "paper" and computer_choice == "rock")
                or (choice == "scissors" and computer_choice == "paper")
                or (choice == "rock" and computer_choice == "scissors")
            ):
                await interaction.response.send_message(
                    f"You choose **{choice}** \n Computer choose **{computer_choice}**! \n You won!"
                )
            else:
                await interaction.response.send_message(
                    f"You choose **{choice}** \n Computer choose **{computer_choice}**! \n Computer won!"
                )

        except Exception as e:
            await interaction.response.send_message(
                f"Unexpected error, **contact support** :- \n {e}", ephemeral=True
            )
