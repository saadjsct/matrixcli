#!/bin/python3

import os
import sys
import gi
import pprint
import mimetypes
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi
from matrix_client.user import User

sys.path.append(os.getenv('HOME')+'/.config/matrixcli/')

def get_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="command line matrix client")
    subparsers = parser.add_subparsers(title='subcommands',dest='subcommand')

    parser.add_argument("-s", "--server", dest="server",
                        help="server to login to")

    parser.add_argument("-u", "--username", dest="username",
                        help="username to login with")


    parser.add_argument("-p", "--password", dest="password",
                        help="the password")

    parser_send = subparsers.add_parser('send', help='send something to a room')
    parser_send.add_argument("-r", "--room-id", dest="room_id", help='spicify the room id')
    group = parser_send.add_mutually_exclusive_group()
    group.add_argument("-t", "--text", dest="text", action="store_true",
                            help="force the program to treat the content as text message")
    group.add_argument("-f", "--file", dest="file", action="store_true",
                            help="force the program to treat the content as a file")
    parser_send.add_argument("content")

    parser_listen = subparsers.add_parser('listen',
                                          help='listen forever for events')

    parser_rooms = subparsers.add_parser('rooms',
                                         help='get all joined rooms')

    parser_tail = subparsers.add_parser('tail',
                                        help='print last messages')
    parser_tail.add_argument("-r", "--room-id", dest="room_id",
                             help='spicify the room id')

    parser_tail.add_argument("-f", "--follow", dest="follow",
                             action="store_true",
                            help="wait for messages and print them as they come")
    parser_tail.add_argument("-n", "--messages", dest="messages_number", default=10,
                            type=int, choices=range(1, 100),
                             help='print the last specified messages')

    return parser

def so_what_we_do_now(args_server,args_username,args_password):
    try :
        # if there is a configuration file
        import config
        server = config.accounts[0]["server"]
        username = config.accounts[0]["username"]
        password = config.accounts[0]["passeval"]()

        if args_username is not None:
            username = args_username

            indexes = [ index for index, account in enumerate(config.accounts) if account['username']==args_username]
            occurences = len(indexes)
            if occurences == 1:
                server = config.accounts[indexes[0]]['server']
                password = config.accounts[indexes[0]]['passeval']()
            elif occurences == 0:
                if args_password is None or args_server is None:
                    print("we cant find any occurence of username {args_username} in the config file,\nin this case you have to pass the password and server through the command line options", file=sys.stderr)
                    exit(1)
                else:
                    password = args_password
                    server = args_server
            else:
                if args_server is None:
                    server = config.accounts[indexes[0]]["server"]
                    password = config.accounts[indexes[0]]["passeval"]()
                for index in indexes:
                    if config.accounts[index]["server"] == args_server:
                        server = args_server
                        password = config.accounts[index]["passeval"]()
                        break

            if args_password is not None:
                password = args_password
        else:
            if args_password is not None or args_server is not None:
                print("you can't specify password or server without username", file=sys.stderr)
                exit(1)

        return server, username, password
    except ModuleNotFoundError:
        return args_server, args_username, args_password

def str_event(event, show_room=True, new_line=True):
    if event['type'] == "m.room.member":
        if event['membership'] == "join":
            return "{0} joined".format(event['content']['displayname'])
    elif event['type'] == "m.room.message":
        room = client.rooms[event['room_id']]
        sender_name = client.get_user(event["sender"]).get_display_name()

        if len(room.get_joined_members()) > 2 and show_room:
            room_name = "(" + room.display_name + ") "
        else:
            room_name = ""
        _new_line = "\n" if new_line else " "
        if event['content']['msgtype'] == "m.text":
            return "{0} {1}:{2}{3}".format(sender_name, room_name, _new_line, event['content']['body'])
        else:
            download_url = api.get_download_url(event['content']['url'])
            return "{0} {1}:{2} download {3} from {4} ".format(sender_name, room_name, _new_line, event['content']['body'], download_url)
    else:
        return event['type']

def listen_callback(event):
    if event["sender"] != client.user_id:
        Notify.init("matrix")
        event_string = str_event(event)
        Notify.Notification.new(event_string).show()
        Notify.uninit()
    print(event_string)

def on_message(room, event):
    if event["sender"] != client.user_id:
        Notify.init("matrix")
        event_string = str_event(event)
        Notify.Notification.new(event_string).show()
        Notify.uninit()
    print(str_event(event, show_room=False, new_line=False))

def choose_room():
    if args.room_id is not None:
        try:
            room = client.rooms[args.room_id]
            return room
        except KeyError:
            print("this room does not exist or you are not joined\n", file=sys.stderr)
    enum_rooms = print_rooms()
    choice = int(input("enter room number : "))
    print("")
    room = list(enum_rooms)[choice][1][1]
    return room

def print_rooms():
    enum_rooms = list(enumerate(client.rooms.items()))
    for i, (k, v) in enum_rooms:
        print(i, v.display_name , k, sep=" : ")
    print("")
    return enum_rooms

def listen():
    client.add_listener(listen_callback)
    client.listen_forever()

def send():
    room = choose_room()
    if os.path.isfile(args.content) and not args.text:
        filename = os.path.basename(args.content)
        mimetype = mimetypes.guess_type(args.content)[0]

        with open( args.content , 'rb') as fobj:
            content = fobj.read()
        mxc_url = client.upload(content, mimetype)

        mime_func = { "image": room.send_image, "audio": room.send_audio,
                      "video": room.send_video, "text": room.send_file}
        mime_func[os.path.dirname(mimetype)](mxc_url, filename)
    elif not args.file:
        room.send_text(args.content)
    else:
        print("file does not exist", file=sys.stderr)
        exit(1)

def tail():
    room = choose_room()
    if args.messages_number > 10 :
        room.backfill_previous_messages(limit=args.messages_number-10)
    for event in room.events[-1*args.messages_number:]:
        print(str_event(event, new_line=False))
    if args.follow :
        room.add_listener(on_message)
        client.start_listener_thread()

        while True:
            msg = input()
            room.send_text(msg)

#---------main----------

args = get_parser().parse_args()
server, username, password = so_what_we_do_now(args.server, args.username, args.password)

client = MatrixClient(server)
token = client.login(username,password)
api = MatrixHttpApi(server, token)

subcommand = { "listen": listen,
               "rooms": print_rooms,
               "send": send,
               "tail": tail,
               None: print_rooms}

subcommand[args.subcommand]()

