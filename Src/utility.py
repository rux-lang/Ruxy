from discord import Interaction, Member
from config import JAIL_ROLE_ID

def is_jailed(ctx: Interaction) -> bool:
	if ctx.guild is None:
		return False
	return ctx.user.get_role(JAIL_ROLE_ID) is not None