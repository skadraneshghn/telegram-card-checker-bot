from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utilsdf.functions import symbol

text_home = """<b>خوش آمدید »</b>
<code>این ربات بررسی سریع و ایمن کارت‌ها را با درگاه‌های متنوع و ابزارهای کاربردی برای شما ارائه می‌دهد! ✨</code>
                  
<a href='tg://user?id={}'>🔹 <b>نسخه ربات</b> </a> -» <code>1.3</code>"""

exit_button = InlineKeyboardButton("خروج ⚠️", "exit")

buttons_cmds = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("درگاه‌ها ♻️", "gates"),
            InlineKeyboardButton("ابزارها 🛠", "tools"),
        ],
        [InlineKeyboardButton("کانال 💫", url="https://t.me/Was_B3")],
        [exit_button],
    ]
)

buttons_gates = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("احراز هویت (Auth)", "auths"),
            InlineKeyboardButton("شارژی (Charged)", "chargeds"),
        ],
        [InlineKeyboardButton("ویژه (Special)", "specials")],
        [InlineKeyboardButton("بازگشت 🔄", "home")],
        [exit_button],
    ]
)


# RETURN & EXIT GATES
return_and_exit_gates = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("بازگشت 🔄", "gates")],
        [exit_button],
    ]
)

# RETURN HOME & EXIT
return_home_and_exit = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("بازگشت 🔄", "home")],
        [exit_button],
    ]
)


# ================= GATES AUTH =================

text_gates_auth = f"""
<b>درگاه‌های احراز هویت (Auth) - صفحه ۱ از ۲</b>

{symbol("🔹 𝙊𝙙𝙖𝙡𝙞")} -» <code>Shopify -» Auth</code>
دستور: <code>.od</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙄𝙩𝙖𝙘𝙝𝙞")} -» <code>Payflow AVS -» Auth</code>
دستور: <code>.it</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙕𝙪𝙠𝙚𝙨𝙞𝙩𝙤")} -» <code>Shopify -» Auth</code>
دستور: <code>.zu</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘼𝙨𝙩𝙝𝙖𝙧𝙤𝙩𝙝")} -» <code>Shopify -» Auth</code>
دستور: <code>.at</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_auth_page_1 = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("صفحه بعدی ➡️", "auths_2")],
        [InlineKeyboardButton("بازگشت 🔄", "gates")],
        [exit_button],
    ]
)

text_gates_auth_2 = f"""
<b>درگاه‌های احراز هویت (Auth) - صفحه ۲ از ۲</b>

{symbol("🔹 𝘿𝙖𝙧𝙠𝙞𝙩𝙤")} -» <code>Shopify -» Auth</code>
دستور: <code>.dkt</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙃𝙤𝙨𝙝𝙞𝙜𝙖𝙠𝙞")} -» <code>Shopify -» Auth</code>
دستور: <code>.ho</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙆𝙤")} -» <code>Shopify -» Auth</code>
دستور: <code>.ko</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙇𝙮𝙣𝙭")} -» <code>Shopify -» Auth</code>
دستور: <code>.lynx</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙋𝙞𝙘𝙘𝙤𝙡𝙤")} -» <code>Shopify -» Auth</code>
دستور: <code>.pi</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘼𝙪𝙩𝙤 𝙎𝙝𝙤𝙥𝙞𝙛𝙮")} -» <code>Shopify -» Auto Checkout</code>
دستور: <code>.autosh / .sh</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_auth_page_2 = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("⬅️ صفحه قبلی", "auths")],
        [InlineKeyboardButton("بازگشت 🔄", "gates")],
        [exit_button],
    ]
)


# ================= GATES CHARGED =================

text_gates_charged = f"""
<b>درگاه‌های شارژی (Charged) - صفحه ۱ از ۳</b>

{symbol("🔹 𝙋𝙖𝙮𝙋𝙖𝙡")} -» <code>PayPal -» $0.01</code>
دستور: <code>.pp</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙋𝙖𝙮𝙋𝙖𝙡 𝘼")} -» <code>PayPal -» $1.00</code>
دستور: <code>.ppa</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙂𝙝𝙤𝙪𝙡")} -» <code>SquareUp -» $10.00</code>
دستور: <code>.gh</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘽𝙧𝙚𝙣𝙙𝙖")} -» <code>Braintree -» $28.99</code>
دستور: <code>.br</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘼𝙙𝙧𝙞𝙖𝙣𝙖")} -» <code>Shopify -» $1.00</code>
دستور: <code>.adr</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘼𝙠𝙩𝙯")} -» <code>Stripe -» $1.00</code>
دستور: <code>.ak</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_charged_page_1 = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("صفحه بعدی ➡️", "chargeds_2")],
        [InlineKeyboardButton("بازگشت 🔄", "gates")],
        [exit_button],
    ]
)

text_gates_charged_2 = f"""
<b>درگاه‌های شارژی (Charged) - صفحه ۲ از ۳</b>

{symbol("🔹 𝘼𝙨𝙨")} -» <code>Braintree -» $15.00</code>
دستور: <code>.ass</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘿𝙚𝙫𝙞𝙡𝙨𝙓")} -» <code>Stripe -» $5.00</code>
دستور: <code>.dx</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘿𝙅𝘽𝙖𝙗𝙮")} -» <code>Stripe -» $10.00</code>
دستور: <code>.dj</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙃𝙞𝙣𝙖𝙩𝙖")} -» <code>Stripe -» $1.00</code>
دستور: <code>.hn</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙆𝙖")} -» <code>Stripe -» $10.00</code>
دستور: <code>.ka</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙈𝙖𝙞")} -» <code>Stripe -» $1.00</code>
دستور: <code>.mai</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_charged_page_2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⬅️ صفحه قبلی", "chargeds"),
            InlineKeyboardButton("صفحه بعدی ➡️", "chargeds_3"),
        ],
        [InlineKeyboardButton("بازگشت 🔄", "gates")],
        [exit_button],
    ]
)

text_gates_charged_3 = f"""
<b>درگاه‌های شارژی (Charged) - صفحه ۳ از ۳</b>

{symbol("🔹 𝙋𝙚𝙥𝙚")} -» <code>Stripe -» $1.00</code>
دستور: <code>.pe</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙋𝙪𝙨𝙨𝙮")} -» <code>Stripe -» $1.00</code>
دستور: <code>.ps</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙍𝙤𝙝𝙚𝙚")} -» <code>Stripe -» $1.00</code>
دستور: <code>.rh</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙎𝙚𝙗𝙖𝙨")} -» <code>Stripe -» $1.00</code>
دستور: <code>.sb</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙎𝙚𝙭𝙤")} -» <code>Stripe -» $1.00</code>
دستور: <code>.sexo</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙎𝙎𝙃")} -» <code>Stripe -» $1.00</code>
دستور: <code>.ssh</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_charged_page_3 = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("⬅️ صفحه قبلی", "chargeds_2")],
        [InlineKeyboardButton("بازگشت 🔄", "gates")],
        [exit_button],
    ]
)


# ================= GATES SPECIALS =================

text_gates_especials = f"""
<b>درگاه‌های ویژه و چک دسته‌جمعی</b>

{symbol("🔹 𝙊𝙧𝙤𝙘𝙝𝙞𝙢𝙖𝙧𝙪")} -» <code>Stripe[CCN] -» $1.00</code>
دستور: <code>.or</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘽𝙤𝙧𝙪𝙩𝙤")} -» <code>Stripe[CCN] -» $26.29</code>
دستور: <code>.bo</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙑𝘽𝙑 / 3𝘿𝙎")} -» <code>3DS Lookup</code>
دستور: <code>.vbv</code> -» <code>ویژه</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙈𝙖𝙨𝙨 𝘾𝙝𝙚𝙘𝙠")} -» <code>بررسی دسته‌جمعی کارت‌ها</code>
دستور: <code>.ms</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙈𝙖𝙨𝙨 𝘼𝙙𝙢𝙞𝙣")} -» <code>بررسی دسته‌جمعی مدیریتی</code>
دستور: <code>.msa</code> -» <code>مدیر</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_specials_page_1 = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("بازگشت 🔄", "gates")],
        [exit_button],
    ]
)


# ================= TOOLS =================

text_tools = f"""
<b>ابزارها 🛠 (صفحه ۱ از ۲)</b>

{symbol("🔹 𝙍𝙚𝙛𝙚")} -» <code>ارسال بازخورد و رضایت</code>
دستور: <code>.refe</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘽𝙞𝙣")} -» <code>اطلاعات BIN</code>
دستور: <code>.bin</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙂𝘽𝙞𝙣")} -» <code>ساخت BIN</code>
دستور: <code>.gbin</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘾𝘾 𝙂𝙚𝙣")} -» <code>ساخت کارت اعتباری</code>
دستور: <code>.gen</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙎𝙠")} -» <code>بررسی کلید استرایپ (Stripe Key)</code>
دستور: <code>.sk</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘼𝙙𝙙𝙧𝙚𝙨𝙨")} -» <code>ساخت آدرس فیک</code>
دستور: <code>.rnd us</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_tools_page_1 = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("صفحه بعدی ➡️", "tools_2")],
        [InlineKeyboardButton("بازگشت 🔄", "home")],
        [exit_button],
    ]
)

text_tools_2 = f"""
<b>ابزارها 🛠 (صفحه ۲ از ۲)</b>

{symbol("🔹 𝙄𝙣𝙛𝙤")} -» <code>اطلاعات کاربر</code>
دستور: <code>.my / .id</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙋𝙡𝙖𝙣")} -» <code>اطلاعات اشتراک کاربر</code>
دستور: <code>.plan</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙋𝙡𝙖𝙣𝙂")} -» <code>اطلاعات اشتراک گروه</code>
دستور: <code>.plang</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝘾𝙡𝙖𝙞𝙢")} -» <code>فعالسازی کلید اشتراک</code>
دستور: <code>.claim</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙏𝙧𝙖𝙣𝙨𝙡𝙖𝙩𝙚")} -» <code>ترجمه متن</code>
دستور: <code>.tr</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>

{symbol("🔹 𝙀𝙭𝙩𝙧𝙖")} -» <code>استخراج اکسترا BIN</code>
دستور: <code>.extra</code> -» <code>رایگان</code>
وضعیت: <code>فعال ✅</code>
"""

buttons_tools_page_2 = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("⬅️ صفحه قبلی", "tools")],
        [InlineKeyboardButton("بازگشت 🔄", "home")],
        [exit_button],
    ]
)
