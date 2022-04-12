from datetime import datetime
import os.path

from mcdreforged.api.types import PluginServerInterface, PlayerCommandSource
from mcdreforged.api.command import Literal

from .config import JrrpConfig


def get_jrrp(string: str):
    now = datetime.now()
    num1 = round((abs((hash("asdfgbn" + str(now.timetuple().tm_yday) + "12#3$45" + str(now.year) + "IUY") / 3.0 + hash("QWERTY" + string + "0*8&6" + str(now.day) + "kjhg") / 3.0) / 527.0) % 1001.0))
    num2 = round(num1 / 969.0 * 99.0) if num1 < 970 else 100
    return num2


def register_jrrp_command(server: PluginServerInterface):
    def reply_jrrp(src: PlayerCommandSource):
        uuid = mc_uuid.onlineUUID(src.player).hex if config.online_mode else mc_uuid.offlineUUID(src.player).hex
        jrrp = get_jrrp(uuid)
        for msg_obj in config.message:
            if eval(msg_obj["expr"], {}, {"jrrp": jrrp}):
                start = msg_obj.get("start") if msg_obj.get("start") else config.start
                end = msg_obj.get("end") if msg_obj.get("end") else config.end
                title = msg_obj.get("title") if msg_obj.get("title") else config.title
                msg = start + str(jrrp) + end
                if title:
                    src.get_server().execute("title {} {}".format(src.player, msg))
                src.reply(msg)

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
