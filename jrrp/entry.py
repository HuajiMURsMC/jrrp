import os.path
import time

from mcdreforged.api.types import PluginServerInterface, PlayerCommandSource
from mcdreforged.api.command import Literal

from .config import JrrpConfig


def rol(num: int, k: int, bits: int = 64):
    b1 = bin(num << k)[2:]
    if len(b1) <= bits:
        return int(b1, 2)
    return int(b1[-bits:], 2)


def get_hash(string: str):
    num = 5381
    num2 = len(string) - 1
    for i in range(num2 + 1):
        num = rol(num, 5) ^ num ^ ord(string[i])
    return num ^ 12218072394304324399


def get_jrrp(string: str):
    now = time.localtime()
    num = round(abs((get_hash("".join([
        "asdfgbn",
        str(now.tm_yday),
        "12#3$45",
        str(now.tm_year),
        "IUY"
    ])) / 3 + get_hash("".join([
        "QWERTY",
        key,
        "0*8&6",
        str(now.tm_mday),
        "kjhg"
    ])) / 3) / 527) % 1001)
    if num >= 970:
        num2 = 100
    else:
        num2 = round(num / 969 * 99)
    return num2


def register_jrrp_command(server: PluginServerInterface):
    def reply_jrrp(src: PlayerCommandSource):
        uuid = mc_uuid.onlineUUID(src.player).hex if config.online_mode else mc_uuid.offlineUUID(src.player).hex
        jrrp = get_jrrp(uuid)
        for msg_obj in config.message:
            if eval(msg_obj["expr"]):
                start = msg_obj.get("start") if msg_obj.get("start") else config.start
                end = msg_obj.get("end") if msg_obj.get("end") else config.end
                title = msg_obj.get("title") if msg_obj.get("title") else config.title
                msg = start + str(jrrp) + end
                if title:
                    src.get_server().execute("title {} {}".format(src.player, msg))
                src.reply(msg)
                break

    config = server.load_config_simple(os.path.join("config", "jrrp.json"),
                                       in_data_folder=False,
                                       target_class=JrrpConfig)
    mc_uuid = server.get_plugin_instance("mc_uuid")
    for command in config.command:
        server.register_command(
            Literal(command)
            .requires(lambda src: src.is_player)
            .runs(reply_jrrp)
        )


def on_load(server: PluginServerInterface, old):
    register_jrrp_command(server)
