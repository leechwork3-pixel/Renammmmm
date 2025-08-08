import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from helper.database import Element_Network
from config import Config, Txt

@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, message: Message):
    user = message.from_user
    await Element_Network.add_user(user.id)

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
    user_id = query.from_user.id

    # Debug print can be disabled or removed in production
    print(f"Callback data received: {data}")

    if data == "home":
        await query.message.edit_text(
            Txt.START_TXT.format(query.from_user.mention),
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
    elif data == "caption":
        await query.message.edit_text(
            Txt.CAPTION_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• sᴜᴘᴘᴏʀᴛ", url='https://t.me/manga_campus_chat'),
                 InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="help")]
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
    # Add other callback cases (premiumx, about, donate, file_names, thumbnail, sequence_help, etc.) similarly
    elif data == "close":
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception:
            # Best effort to delete messages, ignore if fails
            pass
          
