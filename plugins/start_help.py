import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from helper.database import Element_Network
from config import Config, Txt


@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, message: Message):
    user = message.from_user
    await Element_Network.add_user(user.id)

    # Animated intro
    m = await message.reply_text("☎️")
    await asyncio.sleep(0.5)
    await m.edit_text("<code>Dᴇᴠɪʟ ᴍᴀʏ ᴄʀʏ...</code>")
    await asyncio.sleep(0.4)
    await m.edit_text("⚡")
    await asyncio.sleep(0.5)
    await m.edit_text("<code>Jᴀᴄᴋᴘᴏᴛ!!!</code>")
    await asyncio.sleep(0.4)
    await m.delete()

    await message.reply_sticker("CAACAgQAAxkBAAIOsGf5RIq9Zodm25_NfFJGKNFNFJv5AALHGAACukfIUwkk20UPuRnvNgQ")

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
        [InlineKeyboardButton("• ᴘʀᴇᴍɪᴜᴍ •", callback_data='premiumx')],
        [InlineKeyboardButton('• ᴅᴇᴠ', url='https://t.me/Shadow_Blank'),
         InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/manga_campus_chat')],
        [InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about')]
    ])

    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Txt.START_TXT.format(user.mention),
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            Txt.START_TXT.format(user.mention),
            reply_markup=buttons,
            disable_web_page_preview=True
        )


@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data
    user_mention = query.from_user.mention

    if data == "home":
        await query.message.edit_text(
            Txt.START_TXT.format(user_mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
                [InlineKeyboardButton("• ᴘʀᴇᴍɪᴜᴍ •", callback_data='premiumx')],
                [InlineKeyboardButton('• ᴅᴇᴠ', url='https://t.me/Shadow_Blank'),
                 InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/manga_campus_chat')],
                [InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'),
                 InlineKeyboardButton('sᴏᴜʀᴄᴇ •', callback_data='source')]
            ])
        )

    elif data == "help":
        await query.message.edit_text(
            Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
                [InlineKeyboardButton("• sᴇǫᴜᴇɴᴄᴇ ғɪʟᴇs •", callback_data='sequence_help')],
                [InlineKeyboardButton('• ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
                 InlineKeyboardButton('ᴄᴀᴘᴛɪᴏɴ •', callback_data='caption')],
                [InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'),
                 InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ •', callback_data='donate')],
                [InlineKeyboardButton('• ʜᴏᴍᴇ', callback_data='home')]
            ])
        )

    elif data == "caption":
        await query.message.edit_text(
            Txt.CAPTION_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• sᴜᴘᴘᴏʀᴛ", url='https://t.me/manga_campus_chat'),
                 InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
            ])
        )

    elif data == "premiumx":
        await query.message.edit_text(
            Txt.PREMIUM_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 Upgrade", url=Config.SUPPORT_CHAT),
                 InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="home")],
            ])
        )

    elif data == "about":
        await query.message.edit_text(
            Txt.ABOUT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📡 Source", callback_data="source")],
                [InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="home")]
            ])
        )

    elif data == "donate":
        await query.message.edit_text(
            Txt.DONATE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Donate", url='https://t.me/Shadow_Blank')],
                [InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
            ])
        )

    elif data == "file_names":
        await query.message.edit_text(
            Txt.FILENAME_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
            ])
        )

    elif data == "thumbnail":
        await query.message.edit_text(
            Txt.THUMBNAIL_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
            ])
        )

    elif data == "sequence_help":
        await query.message.edit_text(
            Txt.SEQUENCE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
            ])
        )

    elif data == "meta":
        await query.message.edit_text(
            Txt.METADATA_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
            ])
        )

    elif data == "source":
        await query.message.edit_text(
            Txt.SOURCE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="about")]
            ])
        )

    elif data == "close":
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception:
            pass
            
