"""
Gateway Registry for Telegram Card Checker Bot.
Maps gateway commands to their names, categories, prices, and handler functions.
"""

from gates.autosh import autoshopify
from gates.aktz import stripe_gate as aktz_gate
from gates.adriana import adriana
from gates.astharoth import astharoth
from gates.boruto import boruto
from gates.brenda import brenda
from gates.darkito import darkito
from gates.devilsx import devilsx
from gates.djbaby import djbaby
from gates.ghoul import ghoul
from gates.hinata import hinata
from gates.hoshigaki import stripe_gate as hoshigaki_gate
from gates.ka import ka
from gates.ko import ko
from gates.lynx import lynx
from gates.mai import mai
from gates.odali import odali
from gates.pepe import pepe
from gates.piccolo import piccolo
from gates.pp import pp_gate
from gates.pp1 import pp_gate as pp_gate1

from gates.rohee import rohee
from gates.sebas import sebas
from gates.sexo import gate_sexo as sexo

from gates.vbv import vbv
from gates.zukesito import zukesito
from gates.shopifys import get_response_gate, load_gates_data


# Dictionary of standalone custom gates
async def run_autosh(cc, m, y, c):
    return await autoshopify("https://morphe.com", cc, m, y, c, True, 100)

async def run_dynamic_shopify(cc, m, y, c, command):
    return await get_response_gate(command, cc, m, y, c, True, 100)

GATEWAYS = {
    "autosh": {
        "name": "Auto Shopify",
        "category": "Shopify",
        "price": "Auto",
        "func": run_autosh,
        "type": "dict",  # returns dict
    },

    "ak": {
        "name": "Aktz (Stripe)",
        "category": "Charged",
        "price": "$1.00",
        "func": aktz_gate,
        "type": "tuple",  # returns (status, msg)
    },
    "adr": {
        "name": "Adriana (Shopify)",
        "category": "Charged",
        "price": "$3.00",
        "func": adriana,
        "type": "tuple",
    },
    "at": {
        "name": "Astharoth (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": astharoth,
        "type": "tuple",
    },
    "bo": {
        "name": "Boruto (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": boruto,
        "type": "tuple",
    },
    "br": {
        "name": "Brenda (Braintree)",
        "category": "Charged",
        "price": "$28.99",
        "func": brenda,
        "type": "tuple",
    },
    "dkt": {
        "name": "Darkito (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": darkito,
        "type": "tuple",
    },
    "dx": {
        "name": "DevilsX (Stripe)",
        "category": "Charged",
        "price": "$5.00",
        "func": devilsx,
        "type": "tuple",
    },
    "dj": {
        "name": "DJBaby (Stripe)",
        "category": "Charged",
        "price": "$10.00",
        "func": djbaby,
        "type": "tuple",
    },
    "gh": {
        "name": "Ghoul (SquareUp)",
        "category": "Charged",
        "price": "$10.00",
        "func": ghoul,
        "type": "tuple",
    },
    "hn": {
        "name": "Hinata (Stripe)",
        "category": "Charged",
        "price": "$1.00",
        "func": hinata,
        "type": "tuple",
    },
    "ho": {
        "name": "Hoshigaki (Stripe)",
        "category": "Auth",
        "price": "$0.00",
        "func": hoshigaki_gate,
        "type": "tuple",
    },
    "ka": {
        "name": "Kabuto (Braintree)",
        "category": "Charged",
        "price": "$3.99",
        "func": ka,
        "type": "tuple",
    },
    "ko": {
        "name": "Konan (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": ko,
        "type": "tuple",
    },

    "lynx": {
        "name": "Lynx (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": lynx,
        "type": "tuple",
    },
    "mai": {
        "name": "Mai (Stripe)",
        "category": "Charged",
        "price": "$1.00",
        "func": mai,
        "type": "tuple",
    },
    "od": {
        "name": "Odali (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": odali,
        "type": "tuple",
    },
    "pe": {
        "name": "Pepe (Stripe)",
        "category": "Charged",
        "price": "$1.00",
        "func": pepe,
        "type": "tuple",
    },
    "pi": {
        "name": "Piccolo (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": piccolo,
        "type": "tuple",
    },
    "pp": {
        "name": "PayPal",
        "category": "Charged",
        "price": "$0.01",
        "func": pp_gate,
        "type": "tuple",
    },
    "ppa": {
        "name": "PayPal A",
        "category": "Charged",
        "price": "$1.00",
        "func": pp_gate1,
        "type": "tuple",
    },
    "rh": {
        "name": "Rohee (Stripe)",
        "category": "Charged",
        "price": "$1.00",
        "func": rohee,
        "type": "tuple",
    },
    "sb": {
        "name": "Sebas (Stripe)",
        "category": "Charged",
        "price": "$1.00",
        "func": sebas,
        "type": "tuple",
    },
    "sexo": {
        "name": "Sexo (Stripe)",
        "category": "Charged",
        "price": "$1.00",
        "func": sexo,
        "type": "tuple",
    },
    "vbv": {
        "name": "VBV Check",
        "category": "Tools",
        "price": "Free",
        "func": vbv,
        "type": "tuple",
    },
    "zu": {
        "name": "Zukesito (Shopify)",
        "category": "Auth",
        "price": "$0.00",
        "func": zukesito,
        "type": "tuple",
    },
}


# Dynamically register gates from assets/gates.json if not already registered
def get_all_gateways():
    all_gates = GATEWAYS.copy()
    try:
        shopify_gates = load_gates_data()
        for g in shopify_gates:
            cmd = g["cmd"]
            if cmd not in all_gates:
                all_gates[cmd] = {
                    "name": f"{g['gate']} ({g['site']})",
                    "category": "Shopify",
                    "price": "Auto",
                    "func": (lambda c_cmd=cmd: lambda cc, m, y, c: run_dynamic_shopify(cc, m, y, c, c_cmd))(),
                    "type": "string",
                }

    except Exception:
        pass
    return all_gates
