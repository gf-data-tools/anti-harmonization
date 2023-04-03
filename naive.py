import json
import re

from mitmproxy.http import HTTPFlow

try:
    from elisa2.ogas import crypto
except ImportError:
    ELISA = False
else:
    ELISA = True


class Naive:
    def __init__(self) -> None:
        self.sign = None
        if ELISA:
            print("以30/30/30/30进行建造后重启游戏应用客户端配置")
        else:
            print("请自行修改本地文件开启客户端配置")

    def response(self, flow: HTTPFlow):
        url = flow.request.url
        if (
            url.endswith("/index.php")
            and b"<naive_switch>0</naive_switch>" in flow.response.content
        ):
            print("覆写服务端配置")
            flow.response.content = re.sub(
                b"<naive_switch>0</naive_switch>",
                b"<naive_switch>1</naive_switch>",
                flow.response.content,
            )
        elif ELISA:
            if "/Index/getUid" in url:
                if flow.response.content.startswith(b"#"):
                    uid_data = json.loads(crypto.decode(flow.response.content))
                    self.sign = uid_data["sign"]
            elif url.endswith("/Index/index") and self.sign:
                ret = crypto.decode(
                    flow.response.content.decode(encoding="utf-8"), self.sign
                )
                ret = re.sub(
                    r'"naive_build_gun_formula":"(\d+:\d+:\d+:\d+)?"',
                    r'"naive_build_gun_formula":"30:30:30:30"',
                    ret,
                )
                flow.response.content = crypto.encode_comp(ret, self.sign)


addons = [Naive()]
