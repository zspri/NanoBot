from discord.ext import commands
import discord.utils
from __main__ import settings

#
# This is a modified version of checks.py, originally made by Rapptz
#
#                 https://github.com/Rapptz
#          https://github.com/Rapptz/RoboDanny/tree/async
#

def is_owner_check(ctx):
    return ctx.message.author.id == settings.owner

def is_dev_check(ctx):
    if ctx.message.author.id == settings.dev:
        return True
    elif ctx.message.author.id == settings.owner:
        return True
    else:
        return False
    
def is_owner():
    return commands.check(is_owner_check)

def is_dev():
    return commands.check(is_dev_check)

def check_permissions(ctx, perms):
    if is_owner_check(ctx):
        return True
    elif is_dev_check(ctx):
        return True
    elif not perms:
        return False

    ch = ctx.message.channel
    author = ctx.message.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())

def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False

    role = discord.utils.find(check, author.roles)
    return role is not None

def mod_or_permissions(**perms):
    def predicate(ctx):
        server = ctx.message.server
        mod_role = settings.get_server_mod(server).lower()
        admin_role = settings.get_server_admin(server).lower()
        return role_or_permissions(ctx, lambda r: r.name.lower() in (mod_role,admin_role), **perms)

    return commands.check(predicate)

def admin_or_permissions(**perms):
    def predicate(ctx):
        server = ctx.message.server
        admin_role = settings.get_server_admin(server)
        return role_or_permissions(ctx, lambda r: r.name.lower() == admin_role.lower(), **perms)

    return commands.check(predicate)

def serverowner_or_permissions(**perms):
    def predicate(ctx):
        if ctx.message.server is None:
            return False
        server = ctx.message.server
        owner = server.owner

        if ctx.message.author.id == owner.id:
            return True

        return check_permissions(ctx,perms)
    return commands.check(predicate)

def serverowner():
    return serverowner_or_permissions()

def admin():
    return admin_or_permissions()

def mod():
    return mod_or_permissions()
