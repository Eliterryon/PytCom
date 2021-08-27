from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


def chat():
    layout = BoxLayout(orientation='vertical')
    btn1 = Button(text='Hello')
    btn2 = Button(text='World')
    layout.add_widget(btn1)
    layout.add_widget(btn2)