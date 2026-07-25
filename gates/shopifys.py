from gates.autosh import autoshopify
from json import load
from utilsdf.functions import get_bin_info

with open("assets/gates.json", "r", encoding="utf-8-sig") as json_file:
    gates_data = load(json_file)

cmds = set(gate["cmd"] for gate in gates_data)
HEADERS_BASE = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "es,es-ES;q=0.9,en;q=0.8,pt;q=0.7,am;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


async def get_response_gate(
    cmd: str, card: str, month: str, year: str, cvv: str, is_premium: bool, credits: int
) -> str:
    if cmd not in cmds:
        raise ValueError("Cmd not found")
    gate = get_gate_by_cmd(cmd, gates_data)
    site = gate["site"]

    if not site.startswith("https://"):
        site = "https://" + site
    name_gateway = gate["gate"]



    try:
        response = await autoshopify(site, card, month, year, cvv, is_premium, credits)
    except Exception as e:
        return e

    response_gate = (
        response["response"] if response and "response" in response else "UNAVAILABLE"
    )
    total_price = (
        response["total"] if response and "total" in response else "UNAVAILABLE"
    )
    time = response["time"] if response and "time" in response else "UNAVAILABLE"

    cc_formatted = f"{card}|{month}|{year}|{cvv}"

    return f"""<b>🔹 𝘾𝘾 -» <code>{cc_formatted}</code>
🔹 𝙎𝙩𝙖𝙩𝙪𝙨 -» <code>{response["status"]}</code>
🔹 𝙍𝙚𝙨𝙪𝙡𝙩 -» <code>{response_gate}</code>

🔹 𝘽𝙞𝙣 -» <code></code> - <code></code> - <code></code>
🔹 𝘽𝙖𝙣𝙠 -» <code></code>
🔹 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 -» <code></code> 

🔹 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 -» <code>{name_gateway} -» ${total_price[:2]}</code>
🔹 𝙏𝙞𝙢𝙚 -» <code>{time}'s</code>
🔹 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝙗𝙮 -» %s"""



def get_gate_by_cmd(cmd_to_find: str, gates_data) -> dict | None:
    for gate in gates_data:
        if gate["cmd"] == cmd_to_find:
            return gate
    return None
