# Init file for all commands

# from file name import init_function
from .user_cmds import init_user_cmds
from .admin_cmds import init_admin_cmds
from .submit_cmds import init_submit_cmd
from .auto_cmds import init_auto_cmds

def init_cmds(bot):
    init_user_cmds(bot)
    init_admin_cmds(bot)
    init_submit_cmd(bot)
    init_auto_cmds(bot)