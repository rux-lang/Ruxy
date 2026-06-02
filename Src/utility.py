from discord import Interaction, User,Member, Role
from config import JAIL_ROLE_ID, BLOCKED_STRINGS
from blacklist import is_blacklisted, blacklist_user

def is_jailed(ctx: Interaction) -> bool:
	if ctx.guild is None:
		return False
	return ctx.user.get_role(JAIL_ROLE_ID) is not None

def is_allowed(ctx: Interaction, allowed_roles: list[int] = [], allowed_users: list[int] = []) -> bool:
	if ctx.guild is None:
		return False
	
	member: Member = ctx.user # type: ignore
	roles: list[int] = [role.id for role in member.roles]


	if any(id in allowed_roles for id in roles):
		return True # has role
	elif member.id in allowed_users:
		return True # exception has been made
	return False

def filter_inputs(arguments: list[str]) -> bool:
	return any(argument in BLOCKED_STRINGS for argument in arguments)
