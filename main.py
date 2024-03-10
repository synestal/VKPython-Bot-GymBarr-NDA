import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime
from time import sleep
import time
from threading import Thread
import pickle
import yadisk
import os
import requests
import pandas as pd
connect_loop = True
y = yadisk.YaDisk(token="") #Пропишите токен

current_datetime = datetime.now()

token = "" #Пропишите токен

vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, 12345678) #Пропишите id человека
vk = vk_session.get_api()
print(vk_session)
print(longpoll)
print(vk)

if y.exists("/Gbarr") == 0:
    y.mkdir("/Gbarr")

if y.exists("/Gbarr/Исходники") == 0:
    y.mkdir("/Gbarr/Исходники")

if y.exists("/Gbarr/Исходники/1.jpg") == 0:
    y.upload("Исходники/1.jpg", "/Gbarr/Исходники/1.jpg")
if y.exists("/Gbarr/Исходники/2.jpg") == 0:
    y.upload("Исходники/2.jpg", "/Gbarr/Исходники/2.jpg")
if y.exists("/Gbarr/Исходники/3.jpg") == 0:
    y.upload("Исходники/3.jpg", "/Gbarr/Исходники/3.jpg")
if y.exists("/Gbarr/Исходники/4.jpg") == 0:
    y.upload("Исходники/4.jpg", "/Gbarr/Исходники/4.jpg")


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def get_key_map(d, value):
    aboba = {}
    counter1 = 0
    for k, v in d.items():
        for a in v:
            if str(a) == value:
                aboba[k] = {counter1}
                return aboba
        counter1 += 1


def inAndOutYaDisk(userId, filename):
    y.download("/Gbarr/Исходники/" + filename, filename)
    if y.exists("/Gbarr/" + get_key(userListNames, userId) + "/" + filename) == 0:
        y.upload(filename, "/Gbarr/" + get_key(userListNames, userId) + "/" + filename)
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(filename)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    sendPic(userId, attachment)
    os.remove(filename)


def getFromYaDisk(userId, filename):
    try:
        if y.exists("/Gbarr/" + get_key(userListNames, userId) + "/" + filename) == 1:
            y.download("/Gbarr/" + get_key(userListNames, userId) + "/" + filename, filename)
            upload = vk_api.VkUpload(vk)
            photo = upload.photo_messages(filename)
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            sendPic(userId, attachment)
            os.remove(filename)
    except vk_api.exceptions.ApiError:
        print("noneDev")


def getFromYaDisktoDeliver(toWhom, userId, filename):
    try:
        if y.exists("/Gbarr/" + get_key(userListNames, userId) + "/" + filename) == 1:
            y.download("/Gbarr/" + get_key(userListNames, userId) + "/" + filename, filename)
            upload = vk_api.VkUpload(vk)
            photo = upload.photo_messages(filename)
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            sendPic(toWhom, attachment)
            os.remove(filename)
    except vk_api.exceptions.ApiError:
        print("noneDev")

# Создадим функцию для ответа на сообщения в лс группы
def sendText(current_id, supportingText, keyboard_used=None):

    attributes = {
        'user_id': current_id,
        'message': supportingText,
        'random_id': 0
    }

    if keyboard_used is not None:
        attributes["keyboard"] = keyboard_used.get_keyboard()
    else:
        attributes = attributes
    vk_session .method('messages.send', attributes)


def sendTextChat(current_id, supportingText, keyboard_used=None):

    attributes = {
        'chat_id': current_id,
        'message': supportingText,
        'random_id': 0
    }

    if keyboard_used is not None:
        attributes["keyboard"] = keyboard_used.get_keyboard()
    else:
        attributes = attributes
    vk_session .method('messages.send', attributes)


def sendButton(current_id, name, color, text, line):

    keyboard = VkKeyboard(one_time=False)
    a = 0
    for btn, btn_color in zip(name, color):
        if a in line and a != 0:
            keyboard.add_line()
        keyboard.add_button(btn, btn_color)
        a += 1

    sendText(current_id, text, keyboard)


def sendLinkButton(current_id, name, link, text=None):

    if text is not None:
        text = text
    else:
        text = 'Ссылка на видео: '

    keyboardlink = VkKeyboard(one_time=True)
    keyboardlink.add_openlink_button(name, link)
    sendText(current_id, text + link, keyboardlink)


def is_in_text(words, checked_text):
    global trigger_lists
    for trigger in trigger_lists[words]:
        if trigger in checked_text:
            return True
    return False


def is_all_in_text(words, checked_text):
    global trigger_lists
    for trigger in trigger_lists[words]:
        if trigger == checked_text:
            return True
    return False


def sendPic(current_id, supportingText, keyboard_used=None):

    attributes = {
        'user_id': current_id,
        'attachment': supportingText,
        'random_id': 0
    }

    if keyboard_used is not None:
        attributes["keyboard"] = keyboard_used.get_keyboard()
    else:
        attributes = attributes
    vk_session .method('messages.send', attributes)


def sendForTim(spamBase):
    tmr = time.strftime("%H:%M:%S", time.localtime())
    if tmr == "09:00:00":
        for i in spamBase:
            sendTextChat(spamBase[i], "Ежедневная рассылка:  " + snooker)
        sleep(2)


spamBase = {}
userListNames = {}
userListPoints = {}
userListPointsId = {}
userListMaps = {}
weekNow = {}


with open('names.picle', 'rb') as f:
    userListNames = pickle.load(f)
with open('points.picle.', 'rb') as f:
    userListPoints = pickle.load(f)
with open('pointsid.picle', 'rb') as f:
    userListPointsId = pickle.load(f)
with open('pointsmap.picle', 'rb') as f:
    userListMaps = pickle.load(f)
with open('weeknow.picle', 'rb') as f:
    weekNow = pickle.load(f)

print(userListNames)
print(userListPoints)
print(userListPointsId)
print(userListMaps)
print(weekNow)


file = 'список карт (1).xlsx'
map1 = {}
map2 = {}
map3 = {}
map4 = {}
map5 = {}
counter = 0
endpoint = 0
xl = pd.read_excel(file)
names = xl.iloc[counter, 0: 3].tolist()
while not pd.isnull(xl.iloc[counter, 0]):
    if not pd.isnull(xl.iloc[counter, 1]):
        if not pd.isnull(xl.iloc[counter, 2]):
            if names[2] != 'ссылка':
                map1[names[2]] = {names[0], names[1]}
    counter += 1
    names = xl.iloc[counter, 0: 3].tolist()

counter = 0
names = xl.iloc[counter, 5: 8].tolist()
while not pd.isnull(xl.iloc[counter, 5]):
    if not pd.isnull(xl.iloc[counter, 6]):
        if not pd.isnull(xl.iloc[counter, 7]):
            if names[2] != 'ссылка':
                map2[names[2]] = {names[0], names[1]}
    counter += 1
    names = xl.iloc[counter, 5: 8].tolist()

counter = 0
names = xl.iloc[counter, 10: 13].tolist()
while not pd.isnull(xl.iloc[counter, 10]):
    if not pd.isnull(xl.iloc[counter, 11]):
        if not pd.isnull(xl.iloc[counter, 12]):
            if names[2] != 'ссылка':
                map3[names[2]] = {names[0], names[1]}
    counter += 1
    names = xl.iloc[counter, 10: 13].tolist()

counter = 0
names = xl.iloc[counter, 15: 18].tolist()
while not pd.isnull(xl.iloc[counter, 15]):
    if not pd.isnull(xl.iloc[counter, 16]):
        if not pd.isnull(xl.iloc[counter, 17]):
            if names[2] != 'ссылка':
                map4[names[2]] = {names[0], names[1]}
    counter += 1
    names = xl.iloc[counter, 15: 18].tolist()

counter = 0
names = xl.iloc[counter, 20: 23].tolist()
while not pd.isnull(xl.iloc[counter, 20]):
    if not pd.isnull(xl.iloc[counter, 21]):
        if not pd.isnull(xl.iloc[counter, 22]):
            if names[2] != 'ссылка':
                map5[names[2]] = {names[0], names[1]}
    counter += 1
    try:
        names = xl.iloc[counter, 20: 23].tolist()
    except IndexError:
        break


def foo():
    for i in range(100000):
        # print(i)
        # sendForTim(spamBase)
        sleep(1)


Thread(target=foo).start()


def main():
    a = 0
    massToOutput = " "
    cntrToOutput = 0
    for event in longpoll.listen():

        if int(time.strftime('%M')) < 30 and cntrToOutput == 1:
            massToOutput = ""
            cntrToOutput = 0
        if int(time.strftime('%M')) >= 30 and cntrToOutput == 0:
            cntrToOutput = 1

        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message['text'].lower()
            if event.from_chat:
                userId = event.chat_id
                userIdTrue = event.object.message['from_id']
                conversation_message_ids = event.object.message['conversation_message_id']
                peer_id = event.object.message['peer_id']
                user = vk_session.method("users.get", {"user_ids": userIdTrue})
                try:
                    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
                except IndexError:
                    fullname = "bot"
                try:
                    print(time.strftime('%H:%M:%S') + " в беседе от: " + str(fullname) + ": " + message)
                    if userId not in spamBase:
                        spamBase[a] = userId
                        a += 1
                except TypeError:
                    print("no more")
                if 'гбар' in message:
                    print("event_from_chat")
                    # if 'привет' in message:
                    #     sendTextChat(userId, welcome_message)

                if "пушкин" in message:
                    try:
                        vk_session.method('messages.delete', {'chat_id': userIdTrue, 'delete_for_all': 1,
                                                                  'cmids': conversation_message_ids, 'group_id': userId,
                                                                  "peer_id": peer_id})
                        vk.messages.removeChatUser(chat_id=userId, member_id=userIdTrue)
                    except vk_api.exceptions.ApiError:
                        print("admin message")

            else:
                userId = event.object.message['from_id']
                user = vk_session.method("users.get", {"user_ids": userId})
                fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
                if userId in userListPointsId:
                    print(time.strftime('%H:%M:%S') + " от: " + str(fullname) + "/" + str(get_key(userListNames, userId)) + ": " + message)
                    massToOutput += time.strftime('%H:%M:%S') + " от: " + str(fullname) + "/" + str(get_key(userListNames, userId)) + ": " + message + "\n"
                else:
                    print(time.strftime('%H:%M:%S') + " не зарегистрирован от: " + str(fullname) + ": " + message)
                    massToOutput += time.strftime('%H:%M:%S') + " от: " + str(fullname) + "/" + str(get_key(userListNames, userId)) + ": " + message + "\n"
                if 'гбар' in message:
                    try:
                        if 'гбар регистрация ' in message and message.count('гбар регистрация ') == 1:
                            part1, part2 = message.split("гбар регистрация ")
                            if part2 not in userListNames and userId not in userListPointsId and "^" not in part2 and ":" not in part2 and "'" not in part2 and str(userId) in wish_list:
                                userListNames[part2] = userId
                                userListPoints[part2] = 0
                                userListPointsId[userId] = 0
                                sendText(userId, "Успешно зарегистрировано")
                                with open('names.picle', 'wb') as f1:
                                    pickle.dump(userListNames, f1)
                                with open('points.picle', 'wb') as f1:
                                    pickle.dump(userListPoints, f1)
                                with open('pointsid.picle', 'wb') as f1:
                                    pickle.dump(userListPointsId, f1)
                                if str(userId) in person_list['ДжоДжоБарр']:
                                    sendText(userId, "Вы в команде 1")
                                if str(userId) in person_list['Blackminers']:
                                    sendText(userId, "Вы в команде 2")
                                if str(userId) in person_list['Desalientes']:
                                    sendText(userId, "Вы в команде 3")
                                if str(userId) in person_list['GeWinner']:
                                    sendText(userId, "Вы в команде 4")
                                if str(userId) in person_list['Andema']:
                                    sendText(userId, "Вы в команде 5")
                                if str(userId) in person_list['MiniValiki']:
                                    sendText(userId, "Вы в команде 6")
                                if str(userId) in person_list['Ryodanbarr']:
                                    sendText(userId, "Вы в команде 7")
                                if str(userId) in person_list['Скумбрики']:
                                    sendText(userId, "Вы в команде 8")

                                sendText(userId, "Далее напишите команду <гбар выбор карты> для выбора карты")
                            else:
                                sendText(userId, "Пользователь с таким именем уже существует или у вас уже зарегистрирован аккаунт, так же, запрещены знаки : ^ ' в никнейме или вы не участник лиги")
                    except ValueError:
                        sendText(userId, "Не правильная команда")
                    try:
                        if 'гбар логги' == message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            sendText(userId, massToOutput)
                        if 'гбар ген' == message:
                            sendPic(userId, "photo-198071571_457350177")
                        if 'гбар михайлофф' == message:
                            sendPic(userId, "photo-198071571_457351410")
                        if 'гбар повысить' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            if message.count(': ') == 2:
                                part1, part2, part3 = message.split(": ")
                                part3 = part3.replace(' ', '')
                                try:
                                    part3 = int(part3)
                                    if part2 in userListNames.keys() and userListNames[part2] in userListMaps.keys():
                                        temp = userListPoints[part2]
                                        userListPoints[part2] += part3
                                        userListPointsId[userListNames[part2]] += part3

                                        with open('points.picle', 'wb') as f1:
                                            pickle.dump(userListPoints, f1)
                                        with open('pointsid.picle', 'wb') as f1:
                                            pickle.dump(userListPointsId, f1)

                                        sendText(userId, "Количество баллов пользователя после повышения: " + str(userListPoints[part2]))
                                        sendText(userListNames[part2], "Вас повысили, ваше количество баллов равно: " + str(userListPoints[part2]))
                                        if temp < 12 <= userListPoints[part2] or temp < 28 <= userListPoints[part2] or temp < 44 <= userListPoints[part2] or temp < 68 <= userListPoints[part2] or temp < 94 <= userListPoints[part2] or temp < 118 <= userListPoints[part2] or temp < 152 <= userListPoints[part2]:
                                            sendText(userListNames[part2], "Поздравляем, вы вышли на новый уровень")
                                    else:
                                        sendText(userId, "Нет такого человека или команда не <гбар повысить: имя: число>")
                                except ValueError:
                                    sendText(userId, "Нет такого человека или команда не <гбар повысить: имя: число>")
                            else:
                                sendText(userId, "Нет такой команды. Образец: <гбар повысить: андрей: 3>")

                        elif 'гбар повысить' in message:
                            sendText(userId, "Вы не админ")

                        if 'гбар изменить баллы' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            if message.count(': ') == 2:
                                part1, part2, part3 = message.split(": ")
                                part3 = part3.replace(' ', '')
                                try:
                                    part3 = int(part3)
                                    if part2 in userListNames.keys() and userListNames[part2] in userListMaps.keys():
                                        temp = userListPoints[part2]
                                        if part3 < 0:
                                            part3 = part3 * (-1)
                                        userListPoints[part2] = part3
                                        userListPointsId[userListNames[part2]] = part3

                                        with open('points.picle', 'wb') as f1:
                                            pickle.dump(userListPoints, f1)
                                        with open('pointsid.picle', 'wb') as f1:
                                            pickle.dump(userListPointsId, f1)

                                        sendText(userId, "Количество баллов пользователя: " + str(userListPoints[part2]))
                                        sendText(userListNames[part2], "Ваше количество баллов изменилось, ваше количество баллов равно: " + str(userListPoints[part2]))
                                        if temp < 12 <= userListPoints[part2] or temp < 28 <= userListPoints[part2] or temp < 44 <= userListPoints[part2] or temp < 68 <= userListPoints[part2] or temp < 94 <= userListPoints[part2] or temp < 118 <= userListPoints[part2] or temp < 152 <= userListPoints[part2]:
                                            sendText(userListNames[part2], "Поздравляем, вы вышли на новый уровень")
                                    else:
                                        sendText(userId, "Нет такого человека или команда не <гбар изменить баллы: имя: число>")
                                except ValueError:
                                    sendText(userId, "Нет такого человека или команда не <гбар изменить баллы: имя: число>")
                            else:
                                sendText(userId, "Нет такой команды. Образец: <гбар изменить баллы: андрей: 3>")

                        elif 'гбар изменить баллы' in message:
                            sendText(userId, "Вы не админ")

                        if 'гбар понизить' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            if message.count(': ') == 2:
                                part1, part2, part3 = message.split(": ")
                                part3 = part3.replace(' ', '')
                                try:
                                    part3 = int(part3)
                                    if part2 in userListNames.keys():
                                        if userListPoints[part2] > part3 - 1:
                                            userListPoints[part2] -= part3
                                            userListPointsId[userListNames[part2]] -= part3
                                            with open('points.picle', 'wb') as f1:
                                                pickle.dump(userListPoints, f1)
                                            with open('pointsid.picle', 'wb') as f1:
                                                pickle.dump(userListPointsId, f1)

                                            sendText(userId, "Количество баллов пользователя после понижения: " + str(userListPoints[part2]))
                                            sendText(userListNames[part2], "Вас понизили, ваше количество баллов равно: " + str(userListPoints[part2]))

                                        else:
                                            sendText(userId,"Баллы итак были меньше уменьшителя, баллы обнулёны")
                                            userListPoints[part2] = 0
                                            userListPointsId[userListNames[part2]] = 0
                                            with open('points.picle', 'wb') as f1:
                                                pickle.dump(userListPoints, f1)
                                            with open('pointsid.picle', 'wb') as f1:
                                                pickle.dump(userListPointsId, f1)
                                            sendText(userListNames[part2], "Вас понизили, ваше количество баллов равно: " + str(userListPoints[part2]))
                                    else:
                                        sendText(userId, "Нет такого человека или команда не <гбар понизить: имя: число>")
                                except ValueError:
                                    sendText(userId, "Нет такого человека или команда не <гбар повысить: имя: число>")
                            else:
                                sendText(userId, "Нет такой команды. Образец: <гбар понизить: андрей: 3>")
                        elif 'гбар понизить' in message:
                            sendText(userId, "Вы не админ")

                        if 'гбар сообщение' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            if message.count(': ') == 2:
                                part1, part2, part3 = message.split(": ")
                                if part2 in userListNames.keys():
                                    sendText(userListNames[part2], "Админ вам написал: " + part3)
                                    sendText(userId, "Отправлено")
                                else:
                                    sendText(userId, "Нет такого человека")
                            else:
                                sendText(userId, "Нет такой команды. Образец: <гбар сообщение: андрей: привет>")

                        elif 'гбар сообщение' in message:
                            sendText(userId, "Вы не админ")

                        if 'гбар статус админ: ' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            part1, part2 = message.split("гбар статус админ: ")
                            if part2 in userListNames.keys() and userListNames[part2] in userListMaps.keys():
                                sendText(userId, "Баллы " + part2 + ": " + str(userListPoints[part2]))
                                getFromYaDisktoDeliver(userId, userListNames[part2], str(userListMaps[userListNames[part2]]) + ".jpg")
                            else:
                                sendText(userId, "Нет такого человека")
                        elif 'гбар статус' in message:
                            if userId in userListPointsId and userId in userListMaps.keys():
                                sendText(userId, "Баллы: " + str(userListPointsId[userId]))
                                getFromYaDisk(userId, str(userListMaps[userId]) + ".jpg")
                                mass = sorted(userListPoints.items(), key=lambda item: item[1], reverse=True)
                                i = 0
                                keys = [key for key, value in userListNames.items() if value == userId]
                                while i < len(mass):
                                    part1, part2, part3 = str(mass[i]).split("'")
                                    if part2 == keys[0]:
                                        sendText(userId, "Актуальный ранг: " + str(i + 1))
                                        break
                                    i += 1
                            else:
                                sendText(userId, "Вы не зарегистрированы")

                        if 'гбар ранги' in message or 'гбар рейтинг' in message:
                            mass = sorted(userListPoints.items(), key=lambda item: item[1], reverse=True)
                            globalOutput = ""
                            if len(mass) < 10:
                                i = 0
                                while i < len(mass):
                                    part1, part2, part3 = str(mass[i]).split("'")
                                    part3 = part3.replace(", ", "", 1)
                                    part3 = part3.replace(")", "", 1)
                                    globalOutput += "Место " + str(i + 1) + ": " + str(part2) + ", баллы: " + str(part3) + "\n"
                                    i += 1
                            else:
                                i = 0
                                while i < 24:
                                    part1, part2, part3 = str(mass[i]).split("'")
                                    part3 = part3.replace(", ", "", 1)
                                    part3 = part3.replace(")", "", 1)
                                    globalOutput += "Место " + str(i + 1) + ": " + str(part2) + ", баллы: " + str(part3) + "\n"
                                    i += 1
                            sendText(userId, globalOutput)
                        if 'гбар команды' in message:
                            i = 0
                            resultHere = {}
                            team = {}
                            for namess in person_list:
                                resultHere[i] = 0
                                team[i] = namess
                                for namess1 in person_list[namess]:
                                    if int(namess1) in userListPointsId.keys():
                                        resultHere[i] += userListPointsId[int(namess1)]
                                i += 1
                            mass = sorted(resultHere.items(), key=lambda item: item[1], reverse=True)
                            i = 0
                            globalOutput = ""
                            while i < len(mass):
                                globalOutput += str(i + 1) + " место команда: " + str(team[mass[i][0]]) + ", количество очков: " + str(mass[i][1]) + "\n"
                                globalOutput +="Члены команды: " + "\n"
                                outputmass = ""
                                for namess1 in person_list[team[mass[i][0]]]:
                                    if int(namess1) in userListPointsId.keys():
                                        outputmass += str(get_key(userListNames, int(namess1))) + ", "
                                globalOutput += outputmass + "\n"
                                i += 1
                            sendText(userId, globalOutput)

                        if 'гбар карты' in message:
                            sendText(userId, "maps")

                        if 'гбар выбор карты ' in message:
                            part1, part2 = message.split("гбар выбор карты ")
                            a = {1, 2, 3, 4}
                            try:
                                part2 = int(part2)
                                if part2 in a:
                                    if userId not in userListMaps and userId in userListPointsId.keys():
                                        userListMaps[userId] = int(part2)
                                        with open('pointsmap.picle', 'wb') as f1:
                                            pickle.dump(userListMaps, f1)
                                        if y.exists("/Gbarr/" + get_key(userListNames, userId)) == 0:
                                            y.mkdir("/Gbarr/" + get_key(userListNames, userId))
                                        if int(part2) == 1:
                                            inAndOutYaDisk(userId, "1.jpg")
                                        if int(part2) == 2:
                                            inAndOutYaDisk(userId, "2.jpg")
                                        if int(part2) == 3:
                                            inAndOutYaDisk(userId, "3.jpg")
                                        if int(part2) == 4:
                                            inAndOutYaDisk(userId, "4.jpg")
                                        sendText(userId, "Зарегистрировано")
                                    else:
                                        sendText(userId, "Уже выбрана карта или вы не зарегистрировались")
                                else:
                                    sendText(userId, "Не правильный номер карты - номер цифра от 1 до 6")
                            except ValueError:
                                sendText(userId, "Не правильный номер карты - номер цифра от 1 до 6")

                        if 'гбар изменить карту' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            if message.count(': ') == 2:
                                part1, part2, part3 = message.split(": ")
                                part3 = part3.replace(' ', '')
                                a = {1, 2, 3, 4}
                                try:
                                    part3 = int(part3)
                                    if part3 in a:
                                        if part2 in userListNames.keys() and userListNames[part2] in userListMaps.keys():
                                            if y.exists("/Gbarr/" + str(part2) + "/" + str(userListMaps[userListNames[part2]]) + ".jpg") == 1:
                                                y.remove("/Gbarr/" + str(part2) + "/" + str(userListMaps[userListNames[part2]]) + ".jpg")
                                            userListMaps[userListNames[part2]] = int(part3)
                                            with open('pointsmap.picle', 'wb') as f1:
                                                pickle.dump(userListMaps, f1)
                                            if y.exists("/Gbarr/" + get_key(userListNames, userListNames[part2])) == 0:
                                                y.mkdir("/Gbarr/" + get_key(userListNames, userListNames[part2]))
                                            if part3 == 1:
                                                inAndOutYaDisk(userListNames[part2], "1.jpg")
                                            if part3 == 2:
                                                inAndOutYaDisk(userListNames[part2], "2.jpg")
                                            if part3 == 3:
                                                inAndOutYaDisk(userListNames[part2], "3.jpg")
                                            if part3 == 4:
                                                inAndOutYaDisk(userListNames[part2], "4.jpg")
                                            sendText(userId, "Зарегистрировано")
                                        else:
                                            sendText(userId, "Нет такого человека или команда не <гбар изменить карту: имя: число>")
                                    else:
                                        sendText(userId, "Нет такого человека или команда не <гбар изменить карту: имя: число>")
                                except ValueError:
                                    sendText(userId, "Нет такого человека или команда не <гбар изменить карту: имя: число>")
                            else:
                                sendText(userId, "Нет такой команды. Образец: <гбар изменить карту: андрей: 3>")
                        elif 'гбар изменить карту' in message:
                            sendText(userId, "Вы не админ")

                        if 'гбар новая неделя' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            weekNow[228] += 1
                            with open('weeknow.picle', 'wb') as f1:
                                pickle.dump(weekNow, f1)
                            for i in userListMaps.keys():
                                sendText(i, "Началась неделя " + str(weekNow[228]) + ", новая карта:")
                                getFromYaDisk(i, str(userListMaps[i]) + ".jpg")
                        elif 'гбар новая неделя' in message:
                            sendText(userId, "Вы не админ")

                        if 'гбар старая неделя' in message and (userId == 251290001 or userId == 643526050 or userId == 587703197 or userId == 155204743 or userId == 660104564 or userId == 45455518):
                            if weekNow[228] > 0:
                                weekNow[228] -= 1
                                with open('weeknow.picle', 'wb') as f1:
                                    pickle.dump(weekNow, f1)
                                sendText(userId, "Началась неделя " + str(weekNow[228]))
                            else:
                                sendText(userId, "Уже неделя 0")
                        elif 'гбар старая неделя' in message:
                            sendText(userId, "Вы не админ")

                        if 'гбар командный элемент ' in message and userId in userListMaps: # Пока не создана нормальная таблица, это исполнение оригинальное. Когда будет создана - использовать вариант с парсером
                            part1, part2 = message.split("гбар командный элемент ")
                            varnReady = 0
                            if int(userListMaps[userId]) == 1 or int(userListMaps[userId]) == 2 or int(userListMaps[userId]) == 3 or int(userListMaps[userId]) == 4:
                                if weekNow[228] >= 1:
                                    if is_all_in_text("т-фрауде", part2):
                                        varnReady = 1
                                        sendText(userId, tFraudeLink)
                                    elif is_all_in_text("перезосо з", part2):
                                        varnReady = 1
                                        sendText(userId, perezosoZLink)
                                    elif is_all_in_text("едп микс ен х", part2):
                                        varnReady = 1
                                        sendText(userId, edpMixEnXLink)
                                    elif is_all_in_text("каида 180", part2):
                                        varnReady = 1
                                        sendText(userId, caidaOneHundredEightyLink)
                                    elif is_all_in_text("мотос аделанте ен кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, motosAdelanteEnCubitalLink)
                                    elif is_all_in_text("11 2100", part2):
                                        varnReady = 1
                                        sendText(userId, elevenTwoOneHundredLink)
                                    elif is_all_in_text("11 360n", part2):
                                        varnReady = 1
                                        sendText(userId, elevenThreeHundredSixtyNLink)

                                if weekNow[228] >= 2:
                                    if is_all_in_text("фрауде микс ен х", part2):
                                        varnReady = 1
                                        sendText(userId, mixFraudeCLink)
                                    elif is_all_in_text("супра кид ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, supraKidEnContraLink)
                                    elif is_all_in_text("контра чешуя", part2):
                                        varnReady = 1
                                        sendText(userId, contraJeshuaLink)
                                    elif is_all_in_text("пятнадцать", part2):
                                        varnReady = 1
                                        sendText(userId, fiveteenLink)
                                    elif is_all_in_text("арко эстатико фулл ен кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, arcoEstaticoFullEnCubitaLink)
                                    elif is_all_in_text("алемана супрема ен сеудос", part2):
                                        varnReady = 1
                                        sendText(userId, alemanaSupremaEnSeudosLink)
                                    elif is_all_in_text("йойо медио ен кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, medioYoyoEnCubtialLink)
                                    elif is_all_in_text("роллос аделанте ен кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, rollosAdelanteEnSeudoEnCubitalLink)
                                    elif is_all_in_text("ультра 10", part2):
                                        varnReady = 1
                                        sendText(userId, uTenLink)

                                if weekNow[228] >= 3:
                                    if is_all_in_text("реверсо кид", part2):
                                        varnReady = 1
                                        sendText(userId, reversoKidLink)
                                    elif is_all_in_text("есфера", part2):
                                        varnReady = 1
                                        sendText(userId, esferaLink)
                                    elif is_all_in_text("флор ен х", part2):
                                        varnReady = 1
                                        sendText(userId, florEnXLink)
                                    elif is_all_in_text("эскуадра анклада ен контра ен х", part2):
                                        varnReady = 1
                                        sendText(userId, escuadraAncladoEnContraEnXLink)
                                    elif is_all_in_text("кид тарзан микс", part2):
                                        varnReady = 1
                                        sendText(userId, kidTarzanMixLink)
                                    elif is_all_in_text("хорнет кид тарзан ен нормалс", part2):
                                        varnReady = 1
                                        sendText(userId, hornetKidTarzanEnNormalsLink)
                                    elif is_all_in_text("пайсалемана", part2):
                                        varnReady = 1
                                        sendText(userId, piesalemanaLink)
                                    elif is_all_in_text("ультра 10 ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, uTenEnSeudoLink)
                                    elif is_all_in_text("11 с", part2):
                                        varnReady = 1
                                        sendText(userId, elevenCLink)

                                if weekNow[228] >= 4:
                                    if is_all_in_text("уно н супремо", part2):
                                        varnReady = 1
                                        sendText(userId, unoHSupremoLink)
                                    elif is_all_in_text("реверсо кид микс", part2):
                                        varnReady = 1
                                        sendText(userId, reversoKidMixLink)
                                    elif is_all_in_text("сеудо 500", part2):
                                        varnReady = 1
                                        sendText(userId, seudoFiveHundredLink)
                                    elif is_all_in_text("джем ен кубитал-контра", part2):
                                        varnReady = 1
                                        sendText(userId, jemEnCubitalContraLink)
                                    elif is_all_in_text("момиас ен х", part2):
                                        varnReady = 1
                                        sendText(userId, momiasEnXLink)
                                    elif is_all_in_text("гурилера ходжа", part2):
                                        varnReady = 1
                                        sendText(userId, guerilleraHojaLink)
                                    elif is_all_in_text("сийа йойо", part2):
                                        varnReady = 1
                                        sendText(userId, sillaYoyoLink)
                                    elif is_all_in_text("уни камарийа нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, uniKamarillaNiveladaLink)
                                    elif is_all_in_text("медио пронто-у ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, medioProntoYEnSeudoLink)

                                if weekNow[228] >= 5:
                                    if is_all_in_text("инграм", part2):
                                        varnReady = 1
                                        sendText(userId, ingramLink)
                                    elif is_all_in_text("демонио а ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, demonioAEnContraLink)
                                    elif is_all_in_text("кодо серенган", part2):
                                        varnReady = 1
                                        sendText(userId, codoCerenganLink)
                                    elif is_all_in_text("сатан статус p", part2):
                                        varnReady = 1
                                        sendText(userId, satanStatusPLink)
                                    elif is_all_in_text("аркоалемана ен сеудос", part2):
                                        varnReady = 1
                                        sendText(userId, arcoalemanaEnSeudosLink)
                                    elif is_all_in_text("декстер каида 180", part2):
                                        varnReady = 1
                                        sendText(userId, dexterCaidaHundredEightyLink)
                                    elif is_all_in_text("сийа персео супремо", part2):
                                        varnReady = 1
                                        sendText(userId, sillaPerseoSupremoLink)
                                    elif is_all_in_text("кубитал мортеро нивелада ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, cubitalMorteroNiveladaEnSeudoLink)

                                if weekNow[228] >= 6:
                                    if is_all_in_text("унган", part2):
                                        varnReady = 1
                                        sendText(userId, unganLink)
                                    elif is_all_in_text("нс хорнет кид ен контрас", part2):
                                        varnReady = 1
                                        sendText(userId, hsHornetKidEnContrasLink)
                                    elif is_all_in_text("мортеро супремо", part2):
                                        varnReady = 1
                                        sendText(userId, morteroSupremoLink)
                                    elif is_all_in_text("ультра 15", part2):
                                        varnReady = 1
                                        sendText(userId, uFiveteenLink)
                                    elif is_all_in_text("уни крок", part2):
                                        varnReady = 1
                                        sendText(userId, uniCrockLink)
                                    elif is_all_in_text("мортал ен сеудос", part2):
                                        varnReady = 1
                                        sendText(userId, mortalEnSeudosLink)
                                    elif is_all_in_text("аркос аделанте", part2):
                                        varnReady = 1
                                        sendText(userId, arcosAdelanteLink)
                                    elif is_all_in_text("йойо", part2):
                                        varnReady = 1
                                        sendText(userId, yoyoLink)
                                    elif is_all_in_text("инфрамундо т", part2):
                                        varnReady = 1
                                        sendText(userId, inframundoTLink)

                                if weekNow[228] >= 7:
                                    if is_all_in_text("сав", part2):
                                        varnReady = 1
                                        sendText(userId, sawLink)
                                    elif is_all_in_text("шаринган", part2):
                                        varnReady = 1
                                        sendText(userId, sharinganLink)
                                    elif is_all_in_text("сеудо добле кандадо ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, seudoCandadoDobleEnContraLink)
                                    elif is_all_in_text("мортеро ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, morteroEnContraLink)
                                    elif is_all_in_text("катапульта", part2):
                                        varnReady = 1
                                        sendText(userId, catapultaLink)
                                    elif is_all_in_text("вуело дель арко ен х микс", part2):
                                        varnReady = 1
                                        sendText(userId, vueloDelArcoEnXMixLink)
                                    elif is_all_in_text("фрио", part2):
                                        varnReady = 1
                                        sendText(userId, frioLink)
                                    elif is_all_in_text("еньe ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, eneEnContraLink)
                                    elif is_all_in_text("эспайр", part2):
                                        varnReady = 1
                                        sendText(userId, aspireLink)

                                if weekNow[228] >= 8:
                                    if is_all_in_text("кодо б-демонио кит", part2):
                                        varnReady = 1
                                        sendText(userId, codoBDemonioKitLink)
                                    elif is_all_in_text("сингл", part2):
                                        varnReady = 1
                                        sendText(userId, singleLink)
                                    elif is_all_in_text("сеудо кандадо лютор", part2):
                                        varnReady = 1
                                        sendText(userId, seudoCandadoLuthorLink)
                                    elif is_all_in_text("едп статус", part2):
                                        varnReady = 1
                                        sendText(userId, edpStatusLink)
                                    elif is_all_in_text("гирасолес", part2):
                                        varnReady = 1
                                        sendText(userId, girasolesLink)
                                    elif is_all_in_text("стакер", part2):
                                        varnReady = 1
                                        sendText(userId, stuckerLink)
                                    elif is_all_in_text("бумеранг", part2):
                                        varnReady = 1
                                        sendText(userId, boomerangLink)
                                    elif is_all_in_text("мош", part2):
                                        varnReady = 1
                                        sendText(userId, moshLink)
                                    elif is_all_in_text("скрабл инфинити c", part2):
                                        varnReady = 1
                                        sendText(userId, scrableInifnityCLink)

                                if varnReady == 0:
                                    sendText(userId, "Такого элемента нет или не достигнут требуемый уровень прогресса")

                        elif 'гбар командный элемент ' in message:
                            sendText(userId, "Зарегистрируйте карту или напишите правильную команду <гбар выбор карты X>, где X - номер карты от 1 до 4")

                        if 'гбар как выглядит ' in message and userId in userListMaps:
                            part1, part2 = message.split("гбар как выглядит ")
                            varnReady = 0
                            if int(userListMaps[userId]) == 1:
                                temp1 = get_key_map(map1, part2)
                            if int(userListMaps[userId]) == 2:
                                temp1 = get_key_map(map2, part2)
                            if int(userListMaps[userId]) == 3:
                                temp1 = get_key_map(map3, part2)
                            if int(userListMaps[userId]) == 4:
                                temp1 = get_key_map(map4, part2)
                            if temp1 is not None:
                                text = str(list(temp1.values()))
                                symbols_to_remove = "[]{}"
                                for symbol in symbols_to_remove:
                                    text = text.replace(symbol, "")
                                if userListPointsId[userId] >= 0 and weekNow[228] >= 1 and varnReady == 0:
                                    if int(text) < 6:
                                        sendText(userId, temp1.keys())
                                        varnReady = 1

                                if userListPointsId[userId] >= 12 and weekNow[228] >= 1 and varnReady == 0:
                                    if int(text) < 12:
                                        sendText(userId, temp1.keys())
                                        varnReady = 1

                                if userListPointsId[userId] >= 28 and weekNow[228] >= 2 and varnReady == 0:
                                    if int(text) < 18:
                                        sendText(userId, temp1.keys())
                                        varnReady = 1

                                if userListPointsId[userId] >= 44 and weekNow[228] >= 3 and varnReady == 0:
                                    if int(text) < 24:
                                        sendText(userId, temp1.keys())
                                        varnReady = 1

                                if userListPointsId[userId] >= 68 and weekNow[228] >= 4 and varnReady == 0:
                                    if int(text) < 30:
                                        sendText(userId, temp1.keys())
                                        varnReady = 1

                                if userListPointsId[userId] >= 94 and weekNow[228] >= 5 and varnReady == 0:
                                    if int(text) < 36:
                                        sendText(userId, temp1.keys())
                                        varnReady = 1

                                if userListPointsId[userId] >= 118 and weekNow[228] >= 6 and varnReady == 0:
                                    if int(text) < 48:
                                        sendText(userId, temp1.keys())
                                        varnReady = 1

                                # if userListPointsId[userId] >= 152 and weekNow[228] >= 7 and varnReady == 0:
                                    # if int(text) < 48:
                                        # sendText(userId, temp1.keys())
                                        # varnReady = 1
                            if varnReady == 0:
                                sendText(userId, "Такого элемента нет или не достигнут требуемый уровень прогресса")
                        elif 'гбар как выглядит ' in message:
                            sendText(userId, "Зарегистрируйте карту или напишите правильную команду <гбар выбор карты X>, где X - номер карты от 1 до 4")

                        if "гбар упражнения для " in message and userId in userListMaps:
                            part1, part2 = message.split("гбар упражнения для ")
                            varnReady = 0
                            if int(userListMaps[userId]) == 1:
                                if userListPointsId[userId] >= 0 and weekNow[228] >= 1:
                                    if is_all_in_text("перезосо отро", part2):
                                        varnReady = 1
                                        sendText(userId, perezosoOtro)
                                    elif is_all_in_text("кодо т-фрауде", part2):
                                        varnReady = 1
                                        sendText(userId, codoTFraude)
                                    elif is_all_in_text("перезосо", part2):
                                        varnReady = 1
                                        sendText(userId, perezoso)
                                    elif is_all_in_text("фрауде s", part2):
                                        varnReady = 1
                                        sendText(userId, fraudeS)
                                    elif is_all_in_text("кид", part2):
                                        varnReady = 1
                                        sendText(userId, kid)
                                    elif is_all_in_text("демонио", part2):
                                        varnReady = 1
                                        sendText(userId, demonio)

                                if userListPointsId[userId] >= 12 and weekNow[228] >= 2:
                                    if is_all_in_text("фрауде биг мей", part2):
                                        varnReady = 1
                                        sendText(userId, fraudeBigMay)
                                    elif is_all_in_text("кубитал фрауде с", part2):
                                        varnReady = 1
                                        sendText(userId, cubitalFraudeS)
                                    elif is_all_in_text("кит сальтадор оникс", part2):
                                        varnReady = 1
                                        sendText(userId, kiitSaldatorOnix)
                                    elif is_all_in_text("кид анкладо", part2):
                                        varnReady = 1
                                        sendText(userId, kidAnclado)
                                    elif is_all_in_text("супра кид", part2):
                                        varnReady = 1
                                        sendText(userId, supraKid)
                                    elif is_all_in_text("4 анкладо", part2):
                                        varnReady = 1
                                        sendText(userId, fourAnclado)

                                if userListPointsId[userId] >= 28 and weekNow[228] >= 3:
                                    if is_all_in_text("фесферо кандадо супремо", part2):
                                        varnReady = 1
                                        sendText(userId, fesferoKandadoSupremo)
                                    elif is_all_in_text("естей рио", part2):
                                        varnReady = 1
                                        sendText(userId, esteyRio)
                                    elif is_all_in_text("уни сийа анклада", part2):
                                        varnReady = 1
                                        sendText(userId, uniSiyaAnclada)
                                    elif is_all_in_text("сеудо 4 анкладо ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, seudoFourAncladoEnContra)
                                    elif is_all_in_text("демонио ен хирадедос", part2):
                                        varnReady = 1
                                        sendText(userId, demonioEnHiradedos)
                                    elif is_all_in_text("супрас кид", part2):
                                        varnReady = 1
                                        sendText(userId, suprasKid)
                                if userListPointsId[userId] >= 44 and weekNow[228] >= 4:
                                    if is_all_in_text("уно гук", part2):
                                        varnReady = 1
                                        sendText(userId, unoGuk)
                                    elif is_all_in_text("флор фрауде", part2):
                                        varnReady = 1
                                        sendText(userId, florFraude)
                                    elif is_all_in_text("демонио анкладо ен кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, demonioAncladoEnCubital)
                                    elif is_all_in_text("есфера кандадо", part2):
                                        varnReady = 1
                                        sendText(userId, esferaCandado)
                                    elif is_all_in_text("рио пронто", part2):
                                        varnReady = 1
                                        sendText(userId, rioPronto)
                                    elif is_all_in_text("сийа кит", part2):
                                        varnReady = 1
                                        sendText(userId, sillaKit)

                                if userListPointsId[userId] >= 68 and weekNow[228] >= 5:
                                    if is_all_in_text("тапиа фесфера дб", part2):
                                        varnReady = 1
                                        sendText(userId, tapiaFesferaDb)
                                    elif is_all_in_text("уно р", part2):
                                        varnReady = 1
                                        sendText(userId, unoP)
                                    elif is_all_in_text("рио", part2):
                                        varnReady = 1
                                        sendText(userId, rio)
                                    elif is_all_in_text("демонно а", part2):
                                        varnReady = 1
                                        sendText(userId, demonioA)
                                    elif is_all_in_text("термит рапид", part2):
                                        varnReady = 1
                                        sendText(userId, termitRapid)
                                    elif is_all_in_text("сапос аркос кит", part2):
                                        varnReady = 1
                                        sendText(userId, saposArcosKit)

                                if userListPointsId[userId] >= 94 and weekNow[228] >= 6:
                                    if is_all_in_text("ромпе брасо", part2):
                                        varnReady = 1
                                        sendText(userId, rompeBraso)
                                    elif is_all_in_text("уно зум", part2):
                                        varnReady = 1
                                        sendText(userId, unoZoom)
                                    elif is_all_in_text("супра перезосо", part2):
                                        varnReady = 1
                                        sendText(userId, supraPerezoso)
                                    elif is_all_in_text("демонио анкладо эн контра", part2):
                                        varnReady = 1
                                        sendText(userId, demonioAncladoEnContra)
                                    elif is_all_in_text("анти супрас кид", part2):
                                        varnReady = 1
                                        sendText(userId, antiSuprasKid)
                                    elif is_all_in_text("демонио а ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, demonioAEnContra)

                                if userListPointsId[userId] >= 118 and weekNow[228] >= 7:
                                    if is_all_in_text("аполо", part2):
                                        varnReady = 1
                                        sendText(userId, apolo)
                                    elif is_all_in_text("супра сальтадор", part2):
                                        varnReady = 1
                                        sendText(userId, supraSaltador)
                                    elif is_all_in_text("уно p-i", part2):
                                        varnReady = 1
                                        sendText(userId, unoPI)
                                    elif is_all_in_text("эсфера мортеро", part2):
                                        varnReady = 1
                                        sendText(userId, esferaMortero)
                                    elif is_all_in_text("кимера", part2):
                                        varnReady = 1
                                        sendText(userId, quimera)
                                    elif is_all_in_text("эсфера мортеро", part2):
                                        varnReady = 1
                                        sendText(userId, esferaMortero)

                                # if userListPointsId[userId] >= 152 and weekNow[228] >= 8:
                                    # if is_all_in_text("уно у зум", part2):
                                    elif is_all_in_text("уно у зум", part2):
                                        varnReady = 1
                                        sendText(userId, unoYZoom)
                                    elif is_all_in_text("оле инверсо анкладо", part2):
                                        varnReady = 1
                                        sendText(userId, oleInversoAnclado)
                                    elif is_all_in_text("супра кид мортеро анкладо", part2):
                                        varnReady = 1
                                        sendText(userId, supraKidMorteroAnclado)
                                    elif is_all_in_text("инфрамундо глобо", part2):
                                        varnReady = 1
                                        sendText(userId, inframundoGlobo)
                                    elif is_all_in_text("демонио кит", part2):
                                        varnReady = 1
                                        sendText(userId, demonioKit)
                                    elif is_all_in_text("4 кит", part2):
                                        varnReady = 1
                                        sendText(userId, fourKit)

                                if varnReady == 0:
                                    sendText(userId, "Такого элемента нет или не достигнут требуемый уровень прогресса")

                            elif int(userListMaps[userId]) == 2:
                                if userListPointsId[userId] >= 0 and weekNow[228] >= 1:
                                    if is_all_in_text("алемана", part2):
                                        varnReady = 1
                                        sendText(userId, alemana)
                                    elif is_all_in_text("фрио ен дос", part2):
                                        varnReady = 1
                                        sendText(userId, frioEnDos)
                                    elif is_all_in_text("каида", part2):
                                        varnReady = 1
                                        sendText(userId, caida)
                                    elif is_all_in_text("оле каида", part2):
                                        varnReady = 1
                                        sendText(userId, oleCaida)
                                    elif is_all_in_text("мотос", part2):
                                        varnReady = 1
                                        sendText(userId, motos)
                                    elif is_all_in_text("мотос аделанте эн нормалс", part2):
                                        varnReady = 1
                                        sendText(userId, motosAdelanteEnNormals)

                                if userListPointsId[userId] >= 12 and weekNow[228] >= 2:
                                    if is_all_in_text("алемана супрема", part2):
                                        varnReady = 1
                                        sendText(userId, alemanaSuprema)
                                    elif is_all_in_text("алемана микс", part2):
                                        varnReady = 1
                                        sendText(userId, alemanaMix)
                                    elif is_all_in_text("сапокаида", part2):
                                        varnReady = 1
                                        sendText(userId, sapocaida)
                                    elif is_all_in_text("декстер каида", part2):
                                        varnReady = 1
                                        sendText(userId, dexterCaida)
                                    elif is_all_in_text("роллос", part2):
                                        varnReady = 1
                                        sendText(userId, rollos)
                                    elif is_all_in_text("роллос аделанте", part2):
                                        varnReady = 1
                                        sendText(userId, rollosAdelante)

                                if userListPointsId[userId] >= 28 and weekNow[228] >= 3:
                                    if is_all_in_text("сапо", part2):
                                        varnReady = 1
                                        sendText(userId, sapo)
                                    elif is_all_in_text("алемана реверса", part2):
                                        varnReady = 1
                                        sendText(userId, alemanaReversa)
                                    elif is_all_in_text("ходжа", part2):
                                        varnReady = 1
                                        sendText(userId, hoja)
                                    elif is_all_in_text("каида дель мартило", part2):
                                        varnReady = 1
                                        sendText(userId, caidaDelMartillo)
                                    elif is_all_in_text("сийа ен сеудос", part2):
                                        varnReady = 1
                                        sendText(userId, sillaEnSeudos)
                                    elif is_all_in_text("сийа микс аделанте", part2):
                                        varnReady = 1
                                        sendText(userId, sillaMixAdelante)

                                if userListPointsId[userId] >= 44 and weekNow[228] >= 4:
                                    if is_all_in_text("сапо ен х", part2):
                                        varnReady = 1
                                        sendText(userId, sapoEnX)
                                    elif is_all_in_text("хорнет у алемана", part2):
                                        varnReady = 1
                                        sendText(userId, hornetYAlemana)
                                    elif is_all_in_text("нинха каида", part2):
                                        varnReady = 1
                                        sendText(userId, ninjaCaida)
                                    elif is_all_in_text("каида хапонес", part2):
                                        varnReady = 1
                                        sendText(userId, caidaJapones)
                                    elif is_all_in_text("анжелес", part2):
                                        varnReady = 1
                                        sendText(userId, angeles)
                                    elif is_all_in_text("б-момиас", part2):
                                        varnReady = 1
                                        sendText(userId, bMomias)

                                if userListPointsId[userId] >= 68 and weekNow[228] >= 5:
                                    if is_all_in_text("алемана биг мей", part2):
                                        varnReady = 1
                                        sendText(userId, alemanaBigMay)
                                    elif is_all_in_text("аркоалемана", part2):
                                        varnReady = 1
                                        sendText(userId, arcoalemana)
                                    elif is_all_in_text("ходжа 180", part2):
                                        varnReady = 1
                                        sendText(userId, hojaHundredEighty)
                                    elif is_all_in_text("камикаси", part2):
                                        varnReady = 1
                                        sendText(userId, kamikasi)
                                    elif is_all_in_text("зуелас", part2):
                                        varnReady = 1
                                        sendText(userId, zuelas)
                                    elif is_all_in_text("зуелас аделанте микс", part2):
                                        varnReady = 1
                                        sendText(userId, zuelasAdelanteMix)

                                if userListPointsId[userId] >= 94 and weekNow[228] >= 6:
                                    if is_all_in_text("галей", part2):
                                        varnReady = 1
                                        sendText(userId, galley)
                                    elif is_all_in_text("кид алеман тарсан", part2):
                                        varnReady = 1
                                        sendText(userId, kidAlemanTarzan)
                                    elif is_all_in_text("мортал", part2):
                                        varnReady = 1
                                        sendText(userId, mortal)
                                    elif is_all_in_text("декстер каида 180", part2):
                                        varnReady = 1
                                        sendText(userId, dexterCaidaHundredEighty)
                                    elif is_all_in_text("уни сапос", part2):
                                        varnReady = 1
                                        sendText(userId, uniSapos)
                                    elif is_all_in_text("аркос", part2):
                                        varnReady = 1
                                        sendText(userId, arcos)

                                if userListPointsId[userId] >= 118 and weekNow[228] >= 7:
                                    if is_all_in_text("редс алемана реверса ен х-флай", part2):
                                        varnReady = 1
                                        sendText(userId, redsAlemanaReversaEnXFly)
                                    elif is_all_in_text("импульсо супрас эстей", part2):
                                        varnReady = 1
                                        sendText(userId, impulsoSuprasEstey)
                                    elif is_all_in_text("хорнет мортал микс ен х", part2):
                                        varnReady = 1
                                        sendText(userId, hornetMortalMixEnX)
                                    elif is_all_in_text("манжелес аделанте ен кодос", part2):
                                        varnReady = 1
                                        sendText(userId, mangelesAdelanteEnCodos)
                                    elif is_all_in_text("универсалес естей", part2):
                                        varnReady = 1
                                        sendText(userId, universalesEstey)
                                    elif is_all_in_text("кларо 360", part2):
                                        varnReady = 1
                                        sendText(userId, claroThreeHundredSixty)

                                # if userListPointsId[userId] >= 152 and weekNow[228] >= 8:
                                    # if is_all_in_text("суперсеро", part2):
                                    elif is_all_in_text("суперсеро", part2):
                                        varnReady = 1
                                        sendText(userId, supercero)
                                    elif is_all_in_text("виво требюшет", part2):
                                        varnReady = 1
                                        sendText(userId, vivoTrebuchet)
                                    elif is_all_in_text("чит кларо 540", part2):
                                        varnReady = 1
                                        sendText(userId, cheatClaroFiveHundredFourty)
                                    elif is_all_in_text("эклипс", part2):
                                        varnReady = 1
                                        sendText(userId, eclipse)
                                    elif is_all_in_text("сэклипс", part2):
                                        varnReady = 1
                                        sendText(userId, seclipse)
                                    elif is_all_in_text("семимортал аделанте", part2):
                                        varnReady = 1
                                        sendText(userId, semimortalAdelante)

                                if varnReady == 0:
                                    sendText(userId, "Такого элемента нет или не достигнут требуемый уровень прогресса")

                            elif int(userListMaps[userId]) == 4:
                                if userListPointsId[userId] >= 0 and weekNow[228] >= 1:
                                    if is_all_in_text("сеудо кандадо супремо", part2):
                                        varnReady = 1
                                        sendText(userId, seudoCandadoSupremo)
                                    elif is_all_in_text("эскуадра анклада", part2):
                                        varnReady = 1
                                        sendText(userId, escuadraAnclado)
                                    elif is_all_in_text("восемь", part2):
                                        varnReady = 1
                                        sendText(userId, eight)
                                    elif is_all_in_text("ларва", part2):
                                        varnReady = 1
                                        sendText(userId, larva)
                                    elif is_all_in_text("сеудо сатан", part2):
                                        varnReady = 1
                                        sendText(userId, seudoSatan)
                                    elif is_all_in_text("едп ен х", part2):
                                        varnReady = 1
                                        sendText(userId, edpEnX)

                                if userListPointsId[userId] >= 12 and weekNow[228] >= 2:
                                    if is_all_in_text("статус", part2):
                                        varnReady = 1
                                        sendText(userId, status)
                                    elif is_all_in_text("чешуя", part2):
                                        varnReady = 1
                                        sendText(userId, jeshua)
                                    elif is_all_in_text("сеудо 8", part2):
                                        varnReady = 1
                                        sendText(userId, seudoEight)
                                    elif is_all_in_text("шестнадцать", part2):
                                        varnReady = 1
                                        sendText(userId, sixteen)
                                    elif is_all_in_text("тонтин микс", part2):
                                        varnReady = 1
                                        sendText(userId, tontinMix)
                                    elif is_all_in_text("арко эстатико фулл ен сеудос", part2):
                                        varnReady = 1
                                        sendText(userId, arcoEstaticoFullEnSeudos)

                                if userListPointsId[userId] >= 28 and weekNow[228] >= 3:
                                    if is_all_in_text("контра анти краксила кандадо", part2):
                                        varnReady = 1
                                        sendText(userId, contraAntiKraxillaCandado)
                                    elif is_all_in_text("эскуадра анклада с", part2):
                                        varnReady = 1
                                        sendText(userId, escuadraAncladaC)
                                    elif is_all_in_text("уни ларва", part2):
                                        varnReady = 1
                                        sendText(userId, uniLarva)
                                    elif is_all_in_text("флор", part2):
                                        varnReady = 1
                                        sendText(userId, flor)
                                    elif is_all_in_text("десечейбл", part2):
                                        varnReady = 1
                                        sendText(userId, desechable)
                                    elif is_all_in_text("табла ен х", part2):
                                        varnReady = 1
                                        sendText(userId, tablaEnX)

                                if userListPointsId[userId] >= 44 and weekNow[228] >= 4:
                                    if is_all_in_text("пятьсот", part2):
                                        varnReady = 1
                                        sendText(userId, fiveHundred)
                                    elif is_all_in_text("статус супремо", part2):
                                        varnReady = 1
                                        sendText(userId, statusSupremo)
                                    elif is_all_in_text("кобра", part2):
                                        varnReady = 1
                                        sendText(userId, cobra)
                                    elif is_all_in_text("сеудо иглесиа", part2):
                                        varnReady = 1
                                        sendText(userId, seudoIglesia)
                                    elif is_all_in_text("крок ен сеудо пунья ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, crockEnSeudosPuna)
                                    elif is_all_in_text("шоколат", part2):
                                        varnReady = 1
                                        sendText(userId, chocolate)

                                if userListPointsId[userId] >= 68 and weekNow[228] >= 5:
                                    if is_all_in_text("сатан статус к", part2):
                                        varnReady = 1
                                        sendText(userId, satanStatusK)
                                    elif is_all_in_text("добле краксила кандадо", part2):
                                        varnReady = 1
                                        sendText(userId, kraxillaDobleCandado)
                                    elif is_all_in_text("сеудо 8 ен контра", part2):
                                        varnReady = 1
                                        sendText(userId, seudoEightEnContra)
                                    elif is_all_in_text("москито", part2):
                                        varnReady = 1
                                        sendText(userId, mosquito)
                                    elif is_all_in_text("кубитал кит ен отро-контра", part2):
                                        varnReady = 1
                                        sendText(userId, cubitalKitEnOtroContra)
                                    elif is_all_in_text("едп микс муньекас", part2):
                                        varnReady = 1
                                        sendText(userId, edpMixMunecas)

                                if userListPointsId[userId] >= 94 and weekNow[228] >= 6:
                                    if is_all_in_text("500 ен кандадо", part2):
                                        varnReady = 1
                                        sendText(userId, fiveHundredEnCandado)
                                    elif is_all_in_text("кандадо с", part2):
                                        varnReady = 1
                                        sendText(userId, candadoC)
                                    elif is_all_in_text("мортеро", part2):
                                        varnReady = 1
                                        sendText(userId, mortero)
                                    elif is_all_in_text("уни амарийа", part2):
                                        varnReady = 1
                                        sendText(userId, uniAmarilla)
                                    elif is_all_in_text("уни тонтин", part2):
                                        varnReady = 1
                                        sendText(userId, uniTontin)
                                    elif is_all_in_text("апокалипсис табла фулл", part2):
                                        varnReady = 1
                                        sendText(userId, apocalipsisTablaFull)

                                if userListPointsId[userId] >= 118 and weekNow[228] >= 7:
                                    if is_all_in_text("добле кандадо", part2):
                                        varnReady = 1
                                        sendText(userId, candadoDoble)
                                    elif is_all_in_text("куна", part2):
                                        varnReady = 1
                                        sendText(userId, cuna)
                                    elif is_all_in_text("апокалипсис мортеро супремо", part2):
                                        varnReady = 1
                                        sendText(userId, apocalipsisMorteroSupremo)
                                    elif is_all_in_text("чалито", part2):
                                        varnReady = 1
                                        sendText(userId, chalito)
                                    elif is_all_in_text("сеудо снст р сатан", part2):
                                        varnReady = 1
                                        sendText(userId, seudoSnstPSatan)
                                    elif is_all_in_text("едп180", part2):
                                        varnReady = 1
                                        sendText(userId, edpOneHundredEighty)

                                # if userListPointsId[userId] >= 152 and weekNow[228] >= 8:
                                   #  if is_all_in_text("олимпо лютор", part2):
                                    elif is_all_in_text("олимпо лютор", part2):
                                        varnReady = 1
                                        sendText(userId, olimpoLuthor)
                                    elif is_all_in_text("портела", part2):
                                        varnReady = 1
                                        sendText(userId, portela)
                                    elif is_all_in_text("краксила", part2):
                                        varnReady = 1
                                        sendText(userId, kraxila)
                                    elif is_all_in_text("кид а фуерса", part2):
                                        varnReady = 1
                                        sendText(userId, kidAFuerza)
                                    elif is_all_in_text("уни тонтин ен ультра", part2):
                                        varnReady = 1
                                        sendText(userId, uniTontinEnUltra)
                                    elif is_all_in_text("уни арко эстатико сапо", part2):
                                        varnReady = 1
                                        sendText(userId, uniArcoEstaticoSapo)

                                if varnReady == 0:
                                    sendText(userId, "Такого элемента нет или не достигнут требуемый уровень прогресса")

                            elif int(userListMaps[userId]) == 3:
                                if userListPointsId[userId] >= 0 and weekNow[228] >= 1:
                                    if is_all_in_text("десять", part2):
                                        varnReady = 1
                                        sendText(userId, ten)
                                    elif is_all_in_text("контра 10", part2):
                                        varnReady = 1
                                        sendText(userId, contraTen)
                                    elif is_all_in_text("11 нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, elevenNivelada)
                                    elif is_all_in_text("египсиа", part2):
                                        varnReady = 1
                                        sendText(userId, egipsia)
                                    elif is_all_in_text("египсиа инверсо", part2):
                                        varnReady = 1
                                        sendText(userId, egipsiaInverso)
                                    elif is_all_in_text("египсиа инверсо ен нормал", part2):
                                        varnReady = 1
                                        sendText(userId, egipsiaInversoEnNormal)

                                if userListPointsId[userId] >= 12 and weekNow[228] >= 2:
                                    if is_all_in_text("сеудо 11 нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, seudoElevenNivelada)
                                    elif is_all_in_text("амарийа нивелада ен кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, amarillaNiveladaEnCubital)
                                    elif is_all_in_text("амарийа нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, amarillaNivelada)
                                    elif is_all_in_text("360н", part2):
                                        varnReady = 1
                                        sendText(userId, threeHundredSixtyN)
                                    elif is_all_in_text("две тысячи сто", part2):
                                        varnReady = 1
                                        sendText(userId, twoThousendOneHundred)
                                    elif is_all_in_text("мортеро нивелада эн кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, morteroNiveladaEnCubital)

                                if userListPointsId[userId] >= 28 and weekNow[228] >= 3:
                                    if is_all_in_text("10 ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, tenEnSeudo)
                                    elif is_all_in_text("омега 10 ен х", part2):
                                        varnReady = 1
                                        sendText(userId, omegaTenEnX)
                                    elif is_all_in_text("11 нивелада ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, elevenNiveladaEnSeudo)
                                    elif is_all_in_text("мортеро нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, morteroNivelada)
                                    elif is_all_in_text("иглесиа нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, iglesiaNivelada)
                                    elif is_all_in_text("сеудо иглесиа нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, seudoIglesiaNivelada)

                                if userListPointsId[userId] >= 44 and weekNow[228] >= 4:
                                    if is_all_in_text("амарийа нивелада ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, amarillaNiveladaEnSeudo)
                                    elif is_all_in_text("м-ректо 10 ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, mRectoTenEnSeudo)
                                    elif is_all_in_text("мортеро нивелада ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, morteroNiveladaEnSeudo)
                                    elif is_all_in_text("мортеро нивелада супремо", part2):
                                        varnReady = 1
                                        sendText(userId, morteroNiveladaSupremo)
                                    elif is_all_in_text("йойо медио", part2):
                                        varnReady = 1
                                        sendText(userId, yoyoMedio)
                                    elif is_all_in_text("инфрамундо р", part2):
                                        varnReady = 1
                                        sendText(userId, inframundoP)

                                if userListPointsId[userId] >= 68 and weekNow[228] >= 5:
                                    if is_all_in_text("муньека мортеро нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, munecaMorteroNivelada)
                                    elif is_all_in_text("кубитал 11 нивелада ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, cubitalElevenNiveladaEnSeudo)
                                    elif is_all_in_text("ахоркадо сеудо иглесиа нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, ahorcadoSeudoIglesiaNivelada)
                                    elif is_all_in_text("йойо акварио ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, yoyoAquarioEnSeudo)
                                    elif is_all_in_text("скотч", part2):
                                        varnReady = 1
                                        sendText(userId, scotch)
                                    elif is_all_in_text("инфрамундо ен кубитал", part2):
                                        varnReady = 1
                                        sendText(userId, inframundoEnCubital)

                                if userListPointsId[userId] >= 94 and weekNow[228] >= 6:
                                    if is_all_in_text("сеудос муньека 11 нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, seudosMunecaElevenNivelada)
                                    elif is_all_in_text("уни камарийа нивелада добле ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, uniKamarillaNiveladaDobleEnSeudo)
                                    elif is_all_in_text("бултери", part2):
                                        varnReady = 1
                                        sendText(userId, bulltery)
                                    elif is_all_in_text("медио ен сеудо", part2):
                                        varnReady = 1
                                        sendText(userId, medioEnSeudo)
                                    elif is_all_in_text("персео супремо", part2):
                                        varnReady = 1
                                        sendText(userId, perseoSupremo)
                                    elif is_all_in_text("инфрамундо серка", part2):
                                        varnReady = 1
                                        sendText(userId, inframundoC)

                                if userListPointsId[userId] >= 118 and weekNow[228] >= 7:
                                    if is_all_in_text("краксила нивелада", part2):
                                        varnReady = 1
                                        sendText(userId, kraxillaNivelada)
                                    elif is_all_in_text("энье", part2):
                                        varnReady = 1
                                        sendText(userId, ene)
                                    elif is_all_in_text("кодо бумеранг", part2):
                                        varnReady = 1
                                        sendText(userId, codoboomerang)
                                    elif is_all_in_text("йойо кандадо", part2):
                                        varnReady = 1
                                        sendText(userId, yoyoCandado)
                                    elif is_all_in_text("инфрамундо s", part2):
                                        varnReady = 1
                                        sendText(userId, inframundoS)
                                    elif is_all_in_text("скрабл", part2):
                                        varnReady = 1
                                        sendText(userId, scrable)

                                # if userListPointsId[userId] >= 152 and weekNow[228] >= 8:
                                    # if is_all_in_text("магнун инфинити", part2):
                                    elif is_all_in_text("магнун инфинити", part2):
                                        varnReady = 1
                                        sendText(userId, magnunInfinity)
                                    elif is_all_in_text("рк", part2):
                                        varnReady = 1
                                        sendText(userId, rompeColumnas)
                                    elif is_all_in_text("магнун", part2):
                                        varnReady = 1
                                        sendText(userId, magnun)
                                    elif is_all_in_text("инфрамундо н", part2):
                                        varnReady = 1
                                        sendText(userId, inframundoH)
                                    elif is_all_in_text("кобра ен йойо", part2):
                                        varnReady = 1
                                        sendText(userId, cobraEnYoyo)
                                    elif is_all_in_text("йойо зум", part2):
                                        varnReady = 1
                                        sendText(userId, yoyoZoom)

                                if varnReady == 0:
                                    sendText(userId, "Такого элемента нет или не достигнут требуемый уровень прогресса")

                        elif "гбар упражнения для " in message:
                            sendText(userId, "Зарегистрируйте карту или напишите правильную команду <гбар выбор карты X>, где X - номер карты от 1 до 4")
                    except vk_api.exceptions.ApiError:
                        print("flood")
                # Набор команд
                # Отправить сообщение        sendText(id, supportingText)
                # Создать кнопки         sendButton(id, buttonName, color, supportingText, arrayLines), где buttomName, arrayLines и color - массивы данных, а arrayLines - после какого элемента переход на новую строку
                # Создать кнопку со ссылкой и кнопкой назад          sendLinkButton(id, buttonName, link, supportingText)  supportimgText не обязателен, тогда будет воспроизводиться надпись Ссылка на видео: link


photoMap = []

videoMap = []

startMsg = "Привет, я бот официального сообщества Jimbarr в Росии. Для получения списка моих команд напиши Джимбарр"


snooker = 'Бильярд - это мая жызнь. Даб даб даб. https://www.youtube.com/watch?v=reR2yB68m0U'

# Бд в формате
perezosoOtro = 'Анкладо на основной фронтальный и боковой + балансировка поперечная + балансировка продольная '



person_list = {
    #Команды в формате
    'ДжоДжоБарр': ['767872897', '589681590', '363399582']
}

wish_list = {
             #участники лиги
             #админы
             #прочие
}

trigger_lists = {
                     # Бд в формате
                     'гибкость': ['растяжк', 'тяну', 'тяне', 'тяни', 'жидк', 'гибк', 'растяг'],
                 }
while True:
    try:
        vk_session = vk_api.VkApi(token=token)
        longpoll = VkBotLongPoll(vk_session, 12345678) #Пропишите id человека
        vk = vk_session.get_api()
        print(vk_session)
        print(longpoll)
        print(vk)
        main()
    except requests.exceptions.RequestException or vk_api.exceptions.ApiHttpError or vk_api.exceptions.ApiError:
        print("vk upal")
        time.sleep(5)
        continue

