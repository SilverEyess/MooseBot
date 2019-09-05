from typing import Type

from discord.ext.commands import Bot

overrides = {}


def cog_group(name: str):
    """
    Utility decorator for setting the desired display text for a cog in the help command.
    :param name: the desired cog name
    :return: a function that accepts a type and sets its cog name override to the provided string.
    """
    def inner(cls: Type):
        overrides[cls] = name
        return cls

    return inner


def get_cog_group(client: Bot, cog: str):
    """
    :param client: the Discord client instance
    :param cog: the cog's name, as registered in the client
    :return: the cog's display name, or its default name if it has not been overridden
    """
    return overrides.get(type(client.get_cog(cog)), cog)
