from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_USERNAME, AD_LINK
from link_parser import get_real_terabox_link

bot = Client("terabox_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(c, m):
    u = m.from_user
    try:
        mem = await c.get_chat_member(CHANNEL_USERNAME, u.id)
        if mem.status not in ("member","administrator","creator"):
            raise
    except:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
        ])
        return await m.reply("👋 Welcome!\nPlease join our channel first.", reply_markup=kb)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Watch Ad", url=AD_LINK)],
        [InlineKeyboardButton("✅ I’ve Watched the Ad", callback_data="ad_done")]
    ])
    await m.reply("✅ You're already a member! Watch the ad to proceed.", reply_markup=kb)

@bot.on_callback_query(filters.regex("check_join"))
async def check_join(c, cq):
    try:
        mem = await c.get_chat_member(CHANNEL_USERNAME, cq.from_user.id)
        if mem.status in ("member","administrator","creator"):
            await cq.message.delete()
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎬 Watch Ad", url=AD_LINK)],
                [InlineKeyboardButton("✅ I’ve Watched the Ad", callback_data="ad_done")]
            ])
            return await cq.message.reply("✅ Joined! Please watch the ad.", reply_markup=kb)
    except:
        pass
    await cq.answer("❌ You must join the channel first!", show_alert=True)

@bot.on_callback_query(filters.regex("ad_done"))
async def ad_done(c, cq):
    await cq.message.delete()
    await cq.message.reply("✅ Great! Now send me your Terabox link.")

@bot.on_message(filters.text & ~filters.command("start"))
async def handle_link(c, m):
    link = m.text.strip()
    if "terabox.com" not in link:
        return await m.reply("❌ Invalid link.")
    await m.reply("🔄 Processing...")
    real_url = get_real_terabox_link(link)
    if real_url.startswith("http"):
        await m.reply(f"🎬 Download Link:\n{real_url}", disable_web_page_preview=True)
    else:
        await m.reply(real_url)

bot.run()
