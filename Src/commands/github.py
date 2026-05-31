import discord
import requests
from discord import app_commands

# if the value starts with "$", then the following should be interpreted as a key for this
# if a key does not exist, https://github.com/rux-lang/<key> gets checked.
# links in this directory are assumed to be correct and won't be checked.
# value must end with "/{owner}/repo" if it's not an alias -> no branches
REPOS = {
    "rux": "https://github.com/rux-lang/Rux",
    "std": "https://github.com/rux-lamg/Std",
    "windows": "https://github.com/rux-lang/Windows",
    "linux": "https://github.com/rux-lang/Linux",
    "bsd": "https://github.com/rux-lang/BSD",
    "macos": "https://github.com/rux-lang/MacOS",
    "bot": "https://github.com/rux-lang/Ruxy",
    "website": "https://github.com/rux-lang/Web",
    "illumos": "https://github.com/rux-lang/Illumos"

    # alias
}

async def repo_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name="Rux (Compiler)", value="rux"),
        app_commands.Choice(name="Standard Library", value="std"),
        app_commands.Choice(name="Windows Library", value="windows"),
        app_commands.Choice(name="Linux Library", value="linux"),
        app_commands.Choice(name="BSD Library", value="bsd"),
        app_commands.Choice(name="MacOS Library", value="macos"),
        app_commands.Choice(name="Illumos Library", value="illumos"),
        app_commands.Choice(name="Ruxy Bot", value="bot"),
        app_commands.Choice(name="Rux Website", value="website")
    ]



def setup(tree, client):
    @tree.command(
        name="repo",
        description="Get a link to a Rux repository"
    )
    @app_commands.autocomplete(repository=repo_autocomplete)
    async def repo(
        interaction: discord.Interaction,
        repository: str = "rux"
    ):
        
        deferred = False

        url = REPOS.get(repository, "")
        print(f"Start: {url}")
        if url.startswith("$"): # alias
            url = REPOS.get(url.removeprefix("$"))
            print(f"Alias: {url}")
        elif url == "": # empty -> check url
            r_url = f"https://api.github.com/repos/rux-lang/{repository}"
            await interaction.response.defer()
            deferred = True

            # check if a repo exists
            r = requests.get(r_url, headers={"User-Agent": "repo-check"})
            if r.status_code == 200:
                url = f"https://github.com/rux-lang/{repository}"
                print(f"Repo: {url}")
            elif r.status_code == 404:
                # check for any branch with that name
                repos = [r for r in REPOS.values() if not r.startswith("$")]

                for repo in repos:
                    repo_parts = repo.split("/")
                    # "{owner}/{repo}"
                    repo_url = repo_parts[-2] + "/" + repo_parts[-1] # [-2] = owner, [-1] = repo.

                    r_url = f"https://api.github.com/repos/{repo_url}/branches/{repository}"
                    r = requests.get(r_url, headers={"User-Agent": "repo-branch-checker"})
                    if r.status_code == 200:
                        url = f"https://github.com/{repo_url}/tree/{repository}"
                        print(f"Branch: {url}")
                        break # break the loop


        print(f"Done: {url}")
        if url == "":
            if deferred:
                await interaction.followup.send(
                    "Unknown repository.",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Unknown repository.",
                    ephemeral=True
                )
                return

        view = discord.ui.View()

        view.add_item(
            discord.ui.Button(
                label=f"Open {repository}",
                url=url
            )
        )

        embed = discord.Embed(
            title="Repository",
            description=f"Repository: **{repository}**",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="URL",
            value=url,
            inline=False
        )

        if deferred:
            await interaction.followup.send(
                embed=embed,
                view=view
            )
        else:
            await interaction.response.send_message(
                embed=embed,
                view=view
            )