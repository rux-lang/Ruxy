from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import discord
from discord import Interaction, app_commands

EXAMPLES_DIR = Path(__file__).parent.parent / "Examples"

@dataclass(frozen=True, slots=True)
class Example:
    name: str
    code: str

    @property
    def lines(self) -> int:
        return len(self.code.splitlines())

class ExampleRegistry:
    def __init__(self) -> None:
        self._examples: dict[str, Example] = {}
        self.reload()

    def reload(self) -> None:
        self._examples.clear()

        if not EXAMPLES_DIR.exists():
            EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
            return

        for file in EXAMPLES_DIR.glob("*.rux"):
            try:
                self._examples[file.stem] = Example(
                    name=file.stem,
                    code=file.read_text(encoding="utf-8"),
                )
            except Exception as e:
                print(f"Failed to load {file}: {e}")

    def random(self) -> Example:
        return random.choice(list(self._examples.values()))

    def get(self, name: str) -> Example | None:
        return self._examples.get(name)

    def names(self) -> list[str]:
        return sorted(self._examples.keys())

    def count(self) -> int:
        return len(self._examples)

    def total_lines(self) -> int:
        return sum(example.lines for example in self._examples.values())


registry = ExampleRegistry()

async def example_autocomplete(
    interaction: Interaction,
    current: str,
):
    return [
        app_commands.Choice(
            name=name,
            value=name,
        )
        for name in registry.names()
        if current.lower() in name.lower()
    ][:25]

def setup(tree: app_commands.CommandTree, client: discord.Client):

    @tree.command(
        name="example",
        description="Show a Rux example."
    )
    @app_commands.autocomplete(
        name=example_autocomplete
    )
    async def example(
        interaction: Interaction,
        name: str | None = None,
    ):
        if registry.count() == 0:
            await interaction.response.send_message(
                "No examples loaded.",
                ephemeral=True,
            )
            return

        selected = (
            registry.random()
            if name is None
            else registry.get(name)
        )

        if selected is None:
            await interaction.response.send_message(
                f"Example '{name}' not found.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"{selected.name}",
            description="Rux Example",
        )

        embed.add_field(
            name="Code",
            value=f"```cpp\n{selected.code}\n```",
            inline=False,
        )

        embed.add_field(
            name="Statistics",
            value=(
                f"Lines: **{selected.lines}**\n"
                f"Loaded Examples: **{registry.count()}**"
            ),
            inline=False,
        )

        await interaction.response.send_message(
            embed=embed
        )

    @tree.command(
        name="example-list",
        description="List all examples."
    )
    async def example_list(interaction: Interaction):
        names = registry.names()

        if not names:
            await interaction.response.send_message(
                "No examples loaded.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="Available Examples",
            description="\n".join(
                f"• `{name}`"
                for name in names
            ),
        )

        await interaction.response.send_message(
            embed=embed
        )

    @tree.command(
        name="example-reload",
        description="Reload all examples."
    )
    async def example_reload(interaction: Interaction):
        registry.reload()

        await interaction.response.send_message(
            f"Reloaded **{registry.count()}** examples."
        )

    @tree.command(
        name="example-stats",
        description="Example statistics."
    )
    async def example_stats(interaction: Interaction):
        embed = discord.Embed(
            title="Example Statistics"
        )

        embed.add_field(
            name="Examples",
            value=str(registry.count()),
        )

        embed.add_field(
            name="Total Lines",
            value=str(registry.total_lines()),
        )

        await interaction.response.send_message(
            embed=embed
        )