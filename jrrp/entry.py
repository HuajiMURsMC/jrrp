from datetime import datetime

from mcdreforged.api.types import PluginServerInterface
from mcdreforged.api.command import Literal


DEFAULT_CONFIG = {
    "enable": True,
    "online_mode": True,
    "command": "!!jrrp"
}


def get_jrrp(string: str):
    now = datetime.now()
    num1 = round((abs((hash("asdfgbn" + str(now.timetuple().tm_yday) + "12#3$45" + str(now.year) + "IUY") / 3.0 + hash("QWERTY" + string + "0*8&6" + str(now.day) + "kjhg") / 3.0) / 527.0) % 1001.0))
    num2 = round(num1 / 969.0 * 99.0) if num1 < 970 else 100
    return num2


def get_jrrp_msg(uuid: str):
    jrrp = get_jrrp(uuid)
    if jrrp == 100:
        msg = "！100！100！！！！！"
    elif jrrp == 99:
        msg = "！但不是 100……"
    elif jrrp >= 90:
        msg = "！好评如潮！"
    elif jrrp >= 60:
        msg = "！是不错的一天呢！"
    elif jrrp >= 50:
        msg = "！还行啦还行啦。"
    elif jrrp == 50:
        msg = "！五五开……"
    elif jrrp >= 40:
        msg = "！还……还行吧……？"
    elif jrrp >= 11:
        msg = "！呜哇……"
    elif jrrp >= 1:
        msg = "……（没错，是百分制）"
    else:
        msg = "……"
    return "你今天的人品值是：" + str(jrrp) + msg


def on_load(server: PluginServerInterface, old):
    config = server.load_config_simple(default_config=DEFAULT_CONFIG)
    mc_uuid = server.get_plugin_instance("mc_uuid")
    if config["enable"]:
        server.register_command(
            Literal(config["command"])
            .requires(lambda src: src.is_player)
            .runs(lambda src: src.reply(get_jrrp_msg(mc_uuid.onlineUUID(src.player).hex if config["online_mode"] else mc_uuid.offlineUUID(src.player).hex)))
        )
        server.register_help_message(config["command"], "今日人品")
