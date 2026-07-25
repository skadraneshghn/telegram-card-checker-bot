from json import load
from gates.autosh import autoshopify

def load_gates_data():
    try:
        with open("assets/gates.json", "r", encoding="utf-8-sig") as json_file:
            return load(json_file)
    except Exception:
        return []

def get_all_cmds():
    gates = load_gates_data()
    return set(gate["cmd"] for gate in gates)

# For backward compatibility
gates_data = load_gates_data()
cmds = get_all_cmds()

def get_gate_by_cmd(cmd_to_find: str, gates_list=None) -> dict | None:
    if gates_list is None:
        gates_list = load_gates_data()
    for gate in gates_list:
        if gate["cmd"] == cmd_to_find:
            return gate
    return None

async def get_response_gate(
    cmd: str, card: str, month: str, year: str, cvv: str, is_premium: bool, credits: int
) -> str:
    gate = get_gate_by_cmd(cmd)
    if not gate:
        raise ValueError(f"Cmd {cmd} not found")
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
🔹 𝙎𝙩𝙖𝙩𝙪𝙨 -» <code>{response.get("status", "UNAVAILABLE")}</code>
🔹 𝙍𝙚𝙨𝙪𝙡𝙩 -» <code>{response_gate}</code>

🔹 𝘽𝙞𝙣 -» <code></code> - <code></code> - <code></code>
🔹 𝘽𝙖𝙣𝙠 -» <code></code>
🔹 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 -» <code></code> 

🔹 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 -» <code>{name_gateway} -» ${total_price[:5]}</code>
🔹 𝙏𝙞𝙢𝙚 -» <code>{time}'s</code>
🔹 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝙗𝙮 -» %s"""
