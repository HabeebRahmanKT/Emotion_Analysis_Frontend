import PySimpleGUI as Sg
import os
import sys
import sqlite3
import google.generativeai as genai

BUNDLE_DIRECTORY = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

GOOGLE_API_KEY = YOUR_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def home_window():
    # Sg.popup_no_buttons(title="Hello dear, Good to have you",
    #                     auto_close=True, auto_close_duration=1,
    #                     image="//resources//boy.png")

    seq = 0
    chats = []

    response = model.generate_content("Hello!")

    values = [
        chat['message'] for chat in chats
    ]

    layout = [
        [
            Sg.Listbox(key='CHAT_AREA', values=values,
                       expand_x=True, expand_y=True, background_color="#c0e4ed", horizontal_scroll=True)
        ],
        [
            Sg.Text(key="MESSAGE_PACE_HOLDER", text="Share your feelings..."),
            Sg.InputText(key='MESSAGE', expand_x=True, pad=30, do_not_clear=False),
            Sg.Image(key="SEND_BUTTON", source=BUNDLE_DIRECTORY + "\\resources\\send.png",
                     enable_events=True),
        ],
    ]

    window = Sg.Window(title="hello", layout=layout, font=("Gill Sans MT", 14),
                       element_justification="center||bottom", element_padding=(5, 10),
                       grab_anywhere=True, resizable=True, disable_minimize=False)
    window.finalize().maximize()

    while True:
        event, value = window.read()
        if event == 'Exit' or event == Sg.WIN_CLOSED:
            break

        elif event == 'SEND_BUTTON':
            message = value['MESSAGE']

            chats.append(
                {
                    'sequence': seq,
                    'message': message,
                    'from_id': 0
                }
            )

            response = model.generate_content(message)
            chats.append(
                {
                    'sequence': seq + 1,
                    'message': response.text,
                    'from_id': 1
                }
            )


            seq = seq + 2
            print(chats)

            values = [chat['message'] for chat in chats]
            window['CHAT_AREA'].update(values=values)

    window.close()


# def initialize_database():
#     chat_db_conn = sqlite3.connect("chat.db")
#     cursor = chat_db_conn.cursor()
#
#     try:
#         cursor.execute("""CREATE TABLE chat (
#                                     sequence INT UNIQUE,
#                                     message VARCHAR[300],
#                                     from_id INT)""")
#
#     except sqlite3.OperationalError:
#         print("Database already exist")
#
#     finally:
#         home_window()


Sg.theme("LightBlue3")

if __name__ == '__main__':
    home_window()
