import sys
import time
import json
import urllib
import logging
import requests
import threading
import ChatBotModel
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from insa_data import dic_info


### make button
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# /order을 받았을 때 봇이 답하는 메뉴, 버튼 형식으로 응답
def check_order_graph(bot, args):
    try:
        set_menu = []
        set_menu.append(InlineKeyboardButton("그래프_특만기", callback_data="graph_spc"))
        set_menu.append(InlineKeyboardButton("그래프_갑만기", callback_data="graph_gap"))
        set_menu.append(InlineKeyboardButton("그래프_일반", callback_data="graph_gen"))
        set_menu.append(InlineKeyboardButton("그래프_초빙", callback_data="graph_chobing"))
        set_menu.append(InlineKeyboardButton("그래프_유예", callback_data="graph_wait"))
        set_menu.append(InlineKeyboardButton("그래프_비교과", callback_data="graph_non_subject"))
        set_menu_markup = InlineKeyboardMarkup(build_menu(set_menu, len(set_menu) - 1)) 
        
        # 봇의 응답 메세지 
        insa2020.sendMessage(bot.message.chat.id, "자비스입니다.\n무엇을 알려드릴까요?", reply_markup=set_menu_markup)
    except:
        print("error from check_order")

# 버튼을 눌렀을 때 처리하기    
def manager_order_graph(id, data):
    try:
        if data == 'graph_spc':
            comment = dic_info[data]
        elif data == 'graph_gap':
            comment = dic_info[data]
        elif data == 'graph_gen':
            comment = dic_info[data]
        elif data == 'graph_chobing':
            comment = dic_info[data]
        elif data == 'graph_wait':
            comment = dic_info[data]
        elif data == 'graph_non_subject':
            comment = dic_info[data]
        insa2020.sendMessage(id, comment)

    except:
        print("error from manager_order")

# 답장 응답 함수 - 현재 나에게는 필요없음. 삭제대상
def complete_order(id, reply_text, text):
    try:
        comment = reply_text + "의 답장은 " + text + "입니다."        
        insa2020.sendMessage(id, comment)

    except:
        print("error from complete_order")
    

# 버튼을 눌렀을 때
def callback_get(bot, update):
    if bot.callback_query.data=="spc":      # 특만기
        manager_order(bot.callback_query.message.chat.id, 'spc')
    elif bot.callback_query.data=="gap":    # 갑만기
        manager_order(bot.callback_query.message.chat.id, 'gap')
    elif bot.callback_query.data=="gen":    # 일반
        manager_order(bot.callback_query.message.chat.id, 'gen')
    else:
        insa2020.sendMessage(bot.callback_query.message.chat.id, "다음 기회에..")

### text came
def text(bot, update):
    print(bot.message)
    if bot.message.reply_to_message is not None:
        complete_order(bot.message.chat.id, bot.message.reply_to_message.text, bot.message.text)
    else:
        comment = '''
        안녕하세요. 인비스입니다.
2021.3.1자 인사작업 데이터를 그래프와 지도로 보여드립니다.
원하시는 정보를 아래와 같이 명령 할 수 있습니다.

    /그래프 : 특만기 / 갑만기 / 일반 / 초빙교사 / 유예 / 비교과
    /지  도 : 내신현황 / 1희망 현황
    /학교현황 : 유치원 / 초등학교 / 중학교 / 고등학교 / 특수학교
        '''
        insa2020.sendMessage(bot.message.chat.id, comment)

### print log
def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


if __name__ == '__main__':

    insa2020 = ChatBotModel.Insa2020Bot()       # 챗봇 생성 - insa2020
    insa2020.add_handler('graph', check_order_graph)
    insa2020.add_handler('map', check_order_map)
    insa2020.add_handler('school_stat', check_order_school_stat)
    insa2020.add_query_handler(callback_get)
    insa2020.add_message_handler(text)
    insa2020.add_error_handler(error)
    insa2020.start()