from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

Chatbox = BoxLayout(orientation='vertical')


def chat():
    global Chatbox
    Chatbox = BoxLayout(orientation='vertical')
    Chatbox.add_widget(Textbox('bonjour', 'bruno'))
    Chatbox.add_widget(Textbox('bonjour toi', 'antho'))
    Chatbox.add_widget(Textbox('Ca va?', 'bruno'))
    Chatbox.add_widget(Textbox('bien et toi ?', 'antho'))
    Chatbox.add_widget(Textbox('bien', 'bruno'))
    return Chatbox

def Textbox(_text, _name):
    layout = BoxLayout(orientation='horizontal')
    lab1 = Label(text=_name, size=(100,100), size_hint=(None, None))
    lab2 = Label(text=_text, size_hint=(1,1))
    layout.add_widget(lab1)
    layout.add_widget(lab2)
    return layout
