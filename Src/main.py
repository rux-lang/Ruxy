import discord
import typing
from discord import app_commands
from config import TOKEN

from commands import bot_utility, fun, github, moderation, owner, user


class Client(discord.Client):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)
        self.synced = False

    async def setup_hook(self) -> None:
        if self.synced:
            print("setup_hook failed - already synced")
            return
        for guild in self.guilds:
            try:
                tree.copy_global_to(guild=guild)

                synced = await tree.sync(guild=guild)

                print(
                    f"Instantly synced {len(synced)} command(s) to guild: {guild.name}"
                )
            except Exception as e:
                print(f"Failed to sync to guild {guild.name}: {e}")

            self.synced = True

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")
        await self.setup_hook()


intents = discord.Intents.default()

client = Client(intents=intents)

tree = app_commands.CommandTree(client)

bot_utility.setup(tree, client)
user.setup(tree, client)
github.setup(tree, client)
owner.setup(tree, client)
moderation.setup(tree, client)
fun.setup(tree, client)

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set in environment variables.")

client.run(TOKEN)
