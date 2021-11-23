from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import interface.chat as Chat

chat = None


class TestApp(App):
    def build(self):
        global chat

        layout = BoxLayout(orientation="horizontal")
        layout.add_widget(Button(text="yolo", size=(100, 100), size_hint=(None, None)))
        chat = Chat.chat()
        layout.add_widget(chat)
        layout.children
        return layout

    def addChat(self, _profil, _msg):
        global chat

        chat.add_widget(Chat.Textbox(_msg, _profil))


if __name__ == "__main__":
    TestApp().run()
