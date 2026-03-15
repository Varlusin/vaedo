from typing import Dict, Optional, Sequence

Cache: Dict[int, Optional[Sequence[Optional[str]]]] = {
    0: None,
    4: None,
    5: None,
    32: None,
}


def _get_repl_str(
    section: int,
    position: int,
) -> str:
    if Cache[section] == None:
        mod = __import__(
            "TextProcessing.x%03x" % (section), globals(), locals(), ["data"]
        )
        Cache[section] = table = mod.data
    table = Cache[section]
    return table[position]


def _unicodelowersplit(string: str):
    tk_len = 0
    tk = ""
    token_list = []
    lng = {"en": 0, "ru": 0, "hy": 0}
    for index, char in enumerate(string):

        codepoint = ord(char)
        section = codepoint >> 8
        position = codepoint % 256
        if position == 32 and section == 0:
            # handipel e probel
            if tk_len != 0:
                token_list.append(tk)
                tk_len = 0
                tk = ""
            continue
        # probel che
        if section == 0:
            lng["en"] += 1
            tk += _get_repl_str(section=section, position=position)
            tk_len += 1
        if section == 4:
            lng["ru"] += 1
            tk += _get_repl_str(section=section, position=position)
            tk_len += 1
        if section == 5 or section == 32:
            lng["hy"] += 1
            tk += _get_repl_str(section=section, position=position)
            tk_len += 1

    if tk != "":
        token_list.append(tk)
    return max(lng, key=lng.get), token_list
