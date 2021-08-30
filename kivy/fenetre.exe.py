from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from chat import chat

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='horizontal')
        layout.add_widget(chat())
        return layout

TestApp().run()