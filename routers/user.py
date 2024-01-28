import asyncio
import os
import random
from aiogram import Router, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED
from aiogram.types import Message, CallbackQuery, FSInputFile, ChatMemberUpdated
import keyboards
from aiogram.utils.markdown import hlink, hbold
from aiogram.utils.media_group import MediaGroupBuilder

from database.models import User, Stat

MEDIA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    is_new_user = User.add_user(message.chat.id, message.chat.username)
    if is_new_user:
        Stat.increment_stat()

    await message.answer(
        "¡Oferta exclusiva solo para suscriptores de este bot!\n"
        "♻️ Cantidad limitada ♻️\n"
        "Date prisa, quedan 7⃣ plazas",
        reply_markup=keyboards.start()
    )


@router.callback_query(F.data == 'continue')
async def call_continue(call: CallbackQuery):
    url = hlink(call.message.chat.first_name, f'tg://resolve?domain={call.message.chat.username}')
    await call.message.answer_video_note(
        FSInputFile(os.path.join(MEDIA_PATH, 'continue.mp4'))
    )
    await asyncio.sleep(2)

    await call.message.answer(
        f'<b>🚀 ¡Bienvenido, </b>{url} <b>¡Me llamo Alvarez! </b>🚀\n'
        'Si estás leyendo este mensaje, significa que ya estás en camino a GANAR MUCHO DINERO 💰💵\n\n' +
        hbold('👨🏽‍💻 Soy el desarrollador del bot predictor para el juegos Mines, Aviador, Penalty y otros. 👨🏽‍💻 \n') +
        'Mi bot fue creado para la plataforma <u>1XBet</u> solamente.\n\n'
        '¡Cuanto mayor sea su depósito, mayores serán sus ganancias diarias!\n\n'
        'Consigue tu robot gratis \n'
        '👉 @Alvarez_Predictor 👈',
        parse_mode='HTML',
        reply_markup=keyboards.bienvenido()
    )


@router.callback_query(F.data == 'choose_phones')
async def choose_phones(call: CallbackQuery):
    await call.message.answer(
        "Seleccione el sistema operativo:",
        reply_markup=keyboards.phones_select()
    )


@router.callback_query(F.data == 'get_comments')
async def get_comments(call: CallbackQuery):
    group = MediaGroupBuilder()

    for i in range(1, 5):
        group.add_photo(media=FSInputFile(os.path.join(MEDIA_PATH, f'comments{i}.png')))

    await call.message.answer_media_group(group.build())

    group = MediaGroupBuilder()
    for i in range(5, 9):
        group.add_photo(media=FSInputFile(os.path.join(MEDIA_PATH, f'comments{i}.png')))

    await call.message.answer_media_group(group.build())

    await call.message.answer(
        '✅Todos los clientes escriben palabras de agradecimiento después de ganar y se les pide que vuelvan a jugar '
        'con el programa al día siguiente\n'
        '🟢Escríbeme ahora mismo para recoger el programa de forma gratuita',
        reply_markup=keyboards.todos()
    )


@router.callback_query(F.data.startswith('get_phone'))
async def get_phone(call: CallbackQuery):
    if call.data == 'get_phone:android':
        arr = [17, 27, 42, 84]

    if call.data == 'get_phone:ios':
        arr = [13, 29, 53, 78]

    for i in arr:
        await call.message.answer(f'✅ {i} %')
        await asyncio.sleep(random.randint(7, 20)/10)

    await call.message.answer('👇 👇 👇 👇 👇 👇 👇', reply_markup=keyboards.get_me())


@router.callback_query(F.data == 'get_video_notes')
async def get_video_notes(call: CallbackQuery):
    for i in range(1, 4):
        await call.message.answer_video_note(
            FSInputFile(os.path.join(MEDIA_PATH, f'story{i}.mp4')),
            reply_markup=keyboards.get_stories_keyboard()
        )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def check_bot(event: ChatMemberUpdated):
    Stat.add_block_user(event.chat.id)
