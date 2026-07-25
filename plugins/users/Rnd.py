from pyrogram import filters
from pyromod import Client
from pyrogram.types import Message
from utilsdf.db import Database
from utilsdf.functions import get_rand_info
from utilsdf.vars import PREFIXES


@Client.on_message(filters.command("rnd", PREFIXES))
async def rnd(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.is_authorized(user_id, m.chat.id):
            return await m.reply(
                "𝑻𝒉𝒊𝒔 𝒄𝒉𝒂𝒕 𝒊𝒔 𝒏𝒐𝒕 𝒂𝒑𝒑𝒓𝒐𝒗𝒆𝒅 𝒕𝒐 𝒖𝒔𝒆 𝒕𝒉𝒊𝒔 𝒃𝒐𝒕.", quote=True
            )
        # user_info = db.GetInfoUser(user_id)
    text = m.text[len(m.command[0]) + 2 :].strip()

    data = await get_rand_info(text)
    if not data or not data["status"]:
        return await m.reply(get_adresses())

    # domain = data["domain"]
    # nat = data["nat"]
    street = data["street"]
    city = data["city"]
    state = data["state"]
    phone = data["phone"]
    # phone1 = data["phone1"]
    zip_code = data["zip"]
    country = data["country"]
    emoji = data["emoji"]

    await m.reply(
        f"""🔹 𝙎𝙩𝙖𝙩𝙚 -»  <code>{state}</code>
亥 𝘾𝙞𝙩𝙮 -»  <code>{city}</code>
亥 𝙎𝙩𝙧𝙚𝙚𝙩 -» <code>{street}</code>

空 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 -» <code>{country}</code> {emoji}
栗 𝙋𝙝𝙤𝙣𝙚 -» <code>{phone}</code>
北 𝙕𝙞𝙥 -» <code>{zip_code}</code>""",
        quote=True,
    )


def get_adresses() -> str:
    return """
Albania -» al 🇦🇱
Algeria -» dz 🇩🇿
Argentina -» ar 🇦🇷
Armenia -»am 🇦🇲
Australia-» au 🇦🇺
Austria -» at 🇦🇹
Azerbaijan -» az 🇦🇿
Bahamas -» bs 🇧🇸
Bahrain -» bh 🇧🇭
Bangladesh -» bd 🇧🇩
Barbados -» bb 🇧🇧
Belarus -» by 🇧🇾
Belgium -» be 🇧🇪
Bolivia -» bol 🇧🇴
Botswana -» bsw 🇧🇼
Brazil -» br 🇧🇷
Brunei -» bn 🇧🇳
Cambodia -» kh 🇰🇭
Cameroun -» cm 🇨🇲
Canada -» ca 🇨🇦
Chile -» cl 🇨🇱
Colombia -» co 🇨🇴
China -» cn 🇨🇳
Costa Rica -» cr 🇨🇷
Croatia -» hr  🇭🇷
Cuba -» cu 🇨🇺
Cyprus -» cy 🇨🇾
Denmark -» dk 🇩🇰 
Dominican Republic -» do 🇩🇴
DR Congo -» cd 🇨🇩
Ecuador -» ec 🇪🇨
Egypt -» eg 🇪🇬
El Salvador -» sv 🇸🇻
Emirates -» ae 🇦🇪
Estonia -» ee 🇪🇪
Ethiopia -» et 🇪🇹
Fiji -» fj 🇫🇯
Finland -» fi 🇫🇮
France -» fr 🇫🇷
Ghana -» gh 🇬🇭
Guatemala -» gt 🇬🇹
Honduras -» hn 🇭🇳
Hong Kong -» hk 🇭🇰
Hungary -» hu 🇭🇺
India -» in 🇮🇳
Indonesia -» id 🇮🇩
Iran -» ir 🇮🇷
Ireland -» ie 🇮🇪
Israel -» il 🇮🇱
Italy -» it 🇮🇹
Ivory Coast -» kt 🇨🇮
Jamaica -» jm 🇯🇲
Japan -» jp 🇯🇵
Jordan -» jo 🇯🇴
Kazakhstan -» kz 🇰🇿
Kenya -» ke 🇰🇪
Korea -» ko 🇰🇷
Kuwait -» kw 🇰🇼
Latvia -» lv 🇱🇻
Lebanon -» lb 🇱🇧
Lesotho -» ls 🇱🇸
Libya -» ly 🇱🇾
Lithuania -» lt 🇱🇹
Luxembourg -» lu 🇱🇺
Madagascar -» mg 🇲🇬
Malawi -» mw 🇲🇼
Malaysia -» my 🇲🇾
Mali -» ml 🇲🇱
Malta -» mt 🇲🇹
Mauritius -» mu 🇲🇺
México -» mx 🇲🇽
Moldova -» md 🇲🇩
Morocco -» ma 🇲🇦
Myanmar -» mm 🇲🇲
Namibia -» na 🇳🇦
Nepal -» np🇳🇵
Netherlands -» nl 🇳🇱
New Zealand -» nz 🇹🇰
Nicaragua -» ni 🇳🇮
Nigeria -» ng 🇳🇬
Norway -» no 🇳🇴
Oman -» om 🇴🇲
Pakistan -» pk 🇵🇰
Panamá -» pa 🇵🇦
Papua New Guinea -» pg 🇵🇬
Paraguay -» py 🇵🇾
Perú -» pe 🇵🇪
Philippines -» ph 🇵🇭
Poland -» pl 🇵🇱
Portuguese -» pt 🇵🇹
Puerto Rico -» pr 🇵🇷
Qatar -» qa 🇶🇦
Romania -» ro 🇷🇴
Russia -» ru 🇷🇺
Rwanda -» rw 🇷🇼
Saudi Arabia -» sa 🇸🇦
Senegal -» sn 🇸🇳
Singapore -» sg 🇸🇬
Slovakia -» sk 🇪🇺
Slovenia -» si 🇸🇮 
South Africa -» za 🇿🇦
Spain -» es 🇪🇦
Sri Lanka -» lk 🇱🇰
Suriname -» sr 🇸🇷
Sweden -» se 🇸🇪
Switzerland -» ch 🇨🇭
Taiwan(China) -» tw 🇨🇳
Tanzania -» tz 🇹🇿
Thailand -» th 🇹🇭
The Czech Republic -» cz 🇨🇿
The Republic of Iceland -» is 🇮🇸
Trinidad and Tobago -» tt 🇹🇹
Tunisia -» tn 🇹🇳
Turkey -» tr 🇹🇲
Uganda-» ug 🇺🇬
Ukraine -» ua 🇺🇦
United Kingdom -» uk 🇬🇧
United States -» us 🇺🇲
Uruguay -» uy 🇺🇾
Uzbekistan -» uz 🇺🇿
Venezuela -» ve 🇻🇪
Vietnam -» vn 🇻🇳
Yemen -» ye 🇾🇪
Zambia -» zm 🇿🇲
Zimbabwe -» zw 🇿🇼
Киргизия -» kg 🇰🇬
"""
