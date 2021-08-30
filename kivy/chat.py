from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


def chat():
    layout = BoxLayout(orientation='vertical')
    layout.add_widget(Textbox('bonjour', 'bruno'))
    layout.add_widget(Textbox('bonjour toi', 'antho'))
    layout.add_widget(Textbox('Ca va?', 'bruno'))
    layout.add_widget(Textbox('bien et toi ?', 'antho'))
    layout.add_widget(Textbox('bien', 'bruno'))
    return layout

def Textbox(_text, _name):
    layout = BoxLayout(orientation='horizontal')
    lab1 = Label(text=_name, size=(100,100), size_hint=(None, None))
    lab2 = Label(text=_text, size_hint=(1,1))
    layout.add_widget(lab1)
    layout.add_widget(lab2)
    return layout