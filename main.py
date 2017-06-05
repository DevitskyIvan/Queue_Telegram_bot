import telebot
import numpy as np

TOKEN = "397773301:AAFJm8wZ7AdUtkTM0U79ppI59yc_brVxxoo"
bot = telebot.TeleBot(TOKEN)
print(bot.get_me())
quName = np.zeros((0, 1))
currentQueue = "null"
queue = np.zeros((0, 3))
knownUsers = []
userStep = {}
chatStep = {}
commands = {  # command description used in the "help" command
              'start': 'Get used to the bot',
              'help': 'Gives you information about the available commands',
              'new_queue': 'Create new queue',
              'current_queue': 'Gives you name of current queue',
              'select_queue': 'You may change current queue',
              'delete_queue': 'Delete current queue',
              'add_me': 'Add you in current queue',
              'add_new_member': 'Add member in current queue',
              'next_member': 'Delete first member from current queue',
              'check_queue': 'Gives you member from current queue',
}


@bot.message_handler(commands=['new_queue'])
def handle_new_queue(message):
    bot.reply_to(message, 'If you want to create a new queue, enter its name. Or send "No"')
    userStep[message.from_user.id] = 1
    chatStep[message.chat.id] = 1
@bot.message_handler(func=lambda message: ((userStep.get(message.from_user.id) == 1) &
                                           (chatStep.get(message.chat.id) == 1)))
def handle_queue_name(message):
    userStep[message.from_user.id] = 0
    chatStep[message.chat.id] = 0
    if message.text == "No":
        bot.reply_to(message, "New queue wasn't created")
    else:
        global quName
        quName = np.append(quName, [[message.text]], axis=0)
        global currentQueue
        currentQueue = message.text
        bot.reply_to(message, "{0} queue was created".format(message.text))


@bot.message_handler(commands=['select_queue'])
def handle_select_queue(message):
    bot.reply_to(message, 'If you want to change a current queue, enter its name. Or send "No"')
    userStep[message.from_user.id] = 2
    chatStep[message.chat.id] = 1
@bot.message_handler(func=lambda message: ((userStep.get(message.from_user.id) == 2) &
                                           (chatStep.get(message.chat.id) == 1)))
def handle_queue_select(message):
    global currentQueue
    userStep[message.from_user.id] = 0
    chatStep[message.chat.id] = 0
    if message.text == "No":
        bot.reply_to(message, "You don't change current queue. It is {0}".format(currentQueue))
    elif message.text in quName:
        currentQueue = message.text
        bot.reply_to(message, "You change current queue. It is {0}".format(currentQueue))
    else:
        bot.reply_to(message, "{0} queue isn't available. You may look queues on command '/all_queues'".format(message.text))


@bot.message_handler(commands=['delete_queue'])
def handle_delete_queue(message):
    bot.reply_to(message, 'If you want to delete {0} queue, enter "Yes"'.format(currentQueue))
    userStep[message.from_user.id] = 4
    chatStep[message.chat.id] = 1
@bot.message_handler(func=lambda message: ((userStep.get(message.from_user.id) == 4) &
                                           (chatStep.get(message.chat.id) == 1)))
def handle_queue_delete(message):
    global queue
    global currentQueue
    global quName
    userStep[message.from_user.id] = 0
    chatStep[message.chat.id] = 0
    if message.text == "Yes":
        i = 0
        while i != -1:
            print(queue[:, 0])
            i = np.core.defchararray.find(queue[:, 0], currentQueue)
            queue = np.delete(queue, i, 0)
        i = np.core.defchararray.find(quName, currentQueue)
        quName = np.delete(quName, i)
        bot.reply_to(message, "{0} was deleted. Current queue is null".format(currentQueue))
        currentQueue = "null"
    else:
        bot.reply_to(message, "{0} wasn't deleted.".format(currentQueue))


@bot.message_handler(commands=['current_queue'])
def handle_current_queue(message):
    bot.reply_to(message, 'Current queue is {0}'.format(currentQueue))


@bot.message_handler(commands=['add_me'])
def handle_add_me(message):
    global queue
    if currentQueue == "null":
        bot.reply_to(message, "Chose a queue or create new queue\n"
                              "Accepted queues:\n"
                              "{0}".format(quName))
    else:
        queue = np.append(queue, [[currentQueue,
                                   message.from_user.first_name,
                                   message.from_user.last_name]], axis=0)
        qntMembers = queue[:, 0]
        qntMembersCurrent = 0
        for i in range(len(qntMembers)):
            if qntMembers[i] == currentQueue:
                qntMembersCurrent += 1
        bot.reply_to(message, "{0} {1} is {2} in '{3}' queue".format(message.from_user.first_name,
                                                                     message.from_user.last_name,
                                                                     qntMembersCurrent,
                                                                     currentQueue))


@bot.message_handler(commands=['add_new_member'])
def handle_add_member(message):
    bot.reply_to(message, 'If you want to add new member in queue, enter <Name Last_name>. Or send "No"')
    userStep[message.from_user.id] = 3
    chatStep[message.chat.id] = 1
@bot.message_handler(func=lambda message: ((userStep.get(message.from_user.id) == 3) &
                                           (chatStep.get(message.chat.id) == 1)))
def handle_member_add(message):
    global queue
    userStep[message.from_user.id] = 0
    chatStep[message.chat.id] = 0
    t = message.text.split()
    if currentQueue == "null":
        bot.reply_to(message, "Chose a queue or create new queue\n"
                              "Accepted queues:\n"
                              "{0}".format(quName))
    elif message.text == "No":
        bot.reply_to(message, "You don't add new member")
    elif len(t) == 2:
        queue = np.append(queue, [[currentQueue, t[0], t[1]]], axis=0)
        qntMembers = queue[:, 0]
        qntMembersCurrent = 0
        for i in range(len(qntMembers)):
            if qntMembers[i] == currentQueue:
                qntMembersCurrent += 1
        bot.reply_to(message, "{0} {1} is {2} in {3} queue".format(t[0], t[1], qntMembersCurrent, currentQueue))
    else:
        bot.reply_to(message, "Wrong format for member")


@bot.message_handler(commands=['check_queue'])
def handle_check_queue(message):
    k = 0
    que = np.zeros((0, 3))
    for i in range(len(queue[:, 0])):
        if queue[i, 0] == currentQueue:
            k += 1
            part = queue[i, :]
            print(part)
            que = np.append(que, [[k, part[1], part[2]]], axis=0)
    if k == 0:
        bot.reply_to(message, "{0} is empty".format(currentQueue))
    else:
        bot.send_message(message.chat.id, '{0} queue:\n{1}'.format(currentQueue, que))


@bot.message_handler(commands=['next_member'])
def handle_next(message):
    global queue
    qntmembers = queue[:, 0]
    k = -1
    if len(qntmembers) == 0:
        bot.reply_to(message, "The queue '{0}' is empty".format(currentQueue))
    for i in range(len(qntmembers)):
        k += 1
        if qntmembers[i] == currentQueue:
            qntmembers = queue[:, 0]
            if i+1 == len(qntmembers):
                bot.reply_to(message, "{0} {1} left '{2}' queue.\n"
                                      "The queue {3} is empty".format(queue[i, 1],
                                                                      queue[i, 2],
                                                                      currentQueue,
                                                                      currentQueue))
                queue = np.delete(queue, i, 0)
            else:
                for j in queue[i+1:len(qntmembers):1, 0]:
                    k += 1
                    if j == currentQueue:
                        bot.reply_to(message, "{0} {1} left '{2}' queue.\n"
                                              "The next member is {3} {4}".format(queue[i, 1],
                                                                                  queue[i, 2],
                                                                                  currentQueue,
                                                                                  queue[k, 1],
                                                                                  queue[k, 2]))
                        print(queue[i, ...])
                        queue = np.delete(queue, i, 0)
                        break
                if k == len(qntmembers):
                    bot.reply_to(message, "{0} {1} left '{2}' queue.\n"
                                          "The queue {3} is empty".format(queue[i, 1],
                                                                          queue[i, 2],
                                                                          currentQueue,
                                                                          currentQueue))
                    queue = np.delete(queue, i, 0)
                else:
                    break


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could broadcast messages to all users of this bot later
        chatStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, I'm bot for work with queues")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again!")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.chat.id == message.from_user.id:
        bot.reply_to(message, "I don't know this command."
                              "You may look available command in /help")


bot.polling(none_stop=True, interval=0)
