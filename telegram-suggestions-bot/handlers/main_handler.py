import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from config import *
from create_bot import bot
from db.database import session
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from db.crud import *
from keyboard import *


class TicketType(StatesGroup):
    select_ticket_type = State()
    ready_to_input = State()
    question = State()
    memo = State()


async def starting(message: types.Message, state: FSMContext):
    await message.answer(TEXT_MESSAGES['start'], reply_markup=StartKeyboard.markup)
    # await state.set_state(TicketType.select_ticket_type.state)


async def reply_to_user(message: types.Message):
    if MAINTENANCE:
        await message.reply(TEXT_MESSAGES['maintenance'])
        return
    elif not message.reply_to_message.from_user.is_bot or message.is_command():
        return
    elif message.from_user.id not in WHITELIST:
        await message.reply(TEXT_MESSAGES['not_authorized'])
        return
    recipient_id = int(get_ticket_by_message_id(db=session, message_id=str(message.reply_to_message.message_id))[0])
    if not recipient_id:
        await message.reply(TEXT_MESSAGES['outdated'])
        return
    await bot.copy_message(chat_id=recipient_id, from_chat_id=message.chat.id, message_id=message.message_id)
    await message.reply(TEXT_MESSAGES['answer_sent'])
    logging.log(logging.INFO, [message.from_user.id, message.message_id])


async def type_selector(message: types.Message, state: FSMContext):
    if message.text == kind_options[0]:
        await state.update_data(type='question')
        await message.answer(TEXT_MESSAGES['request_question'], reply_markup=GoBackKeyboard.markup)
    elif message.text == kind_options[1]:
        await state.update_data(type='memo')
        await message.answer(TEXT_MESSAGES['request_memo'], reply_markup=GoBackKeyboard.markup)
    elif message.text == kind_options[2]:
        await state.update_data(type='issue')
        await message.answer(TEXT_MESSAGES['request_issue'], reply_markup=GoBackKeyboard.markup)
    else:
        await message.answer(TEXT_MESSAGES['bad_option'])
        return
    await state.set_state(TicketType.ready_to_input.state)


async def forward_handler(message: types.Message, state: FSMContext):
    if message.sticker:
        await message.reply(TEXT_MESSAGES['unsupported_format'])
        return
    if message.text == 'Назад':
        await message.answer(TEXT_MESSAGES["start"], reply_markup=StartKeyboard.markup)
        # await state.set_state(TicketType.select_ticket_type.state)
        await state.finish()
        return
    user_data = await state.get_data()
    if message.text and not message.is_command():
        if user_data['type'] == 'question':
            await message.answer(TEXT_MESSAGES['pending_question'])
            text_user = TEXT_MESSAGES['question_template'].format(message.from_user.username, message.text)
        elif user_data['type'] == 'memo':
            await message.answer(TEXT_MESSAGES['pending_memo'])
            text_user = TEXT_MESSAGES['memo_template'].format(message.from_user.username, message.text)
        elif user_data['type'] == 'issue':
            await message.answer(TEXT_MESSAGES['pending_issue'])
            text_user = TEXT_MESSAGES['issue_template'].format(message.from_user.username, message.text)
        else:
            logging.log(logging.ERROR, 'Здесь чето по пизде поплыло')
            await message.answer(TEXT_MESSAGES['error'])
            return
        bot_reply = await bot.send_message(chat_id=CHAT_ID, parse_mode="HTML", text=text_user,
                                           message_thread_id=TOPIC_ID)
        logging.log(logging.INFO, [message.from_user.id, message.message_id])
    else:
        await message.answer(TEXT_MESSAGES['pending_question'])
        caption = TEXT_MESSAGES['message_template'].format(message.from_user.username,
                                                           message.caption + '\n\n' if message.caption is not None
                                                           else '')
        bot_reply = await bot.copy_message(chat_id=CHAT_ID, from_chat_id=message.from_user.id,
                                           message_id=message.message_id,
                                           caption=caption, parse_mode='HTML', message_thread_id=TOPIC_ID)
    create_ticket(db=session, user_id=str(message.from_user.id), message_id=str(bot_reply['message_id']))
    # await state.set_state(TicketType.select_ticket_type.state)
    await state.finish()
    await message.answer(TEXT_MESSAGES['loop'], reply_markup=StartKeyboard.markup)


def setup_dispatcher(dp: Dispatcher):
    dp.register_message_handler(starting, commands=["start"], chat_type='private')
    dp.register_message_handler(filters.IsReplyFilter(True), filters.IDFilter(chat_id=CHAT_ID), reply_to_user,
                                is_reply=True, content_types=['any'])
    # dp.register_message_handler(starting)

    # dp.register_message_handler(type_selector, state=TicketType.select_ticket_type)
    dp.register_message_handler(type_selector, chat_type='private')
    dp.register_message_handler(forward_handler, chat_type='private', content_types=['any'],
                                state=TicketType.ready_to_input)
