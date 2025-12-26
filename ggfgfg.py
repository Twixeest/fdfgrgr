# telegram_app.py - HTML-like интерфейс в Kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
import json

# ЭТО НАШ "HTML" - KV язык (аналогичен HTML)
kv_code = '''
# Главный контейнер (как <body>)
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        # Шапка (как <header>)
        BoxLayout:
            size_hint_y: 0.1
            canvas.before:
                Color:
                    rgba: 0.07, 0.47, 0.75, 1  # Telegram blue
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            Label:
                text: 'Telegram'
                font_size: '24sp'
                bold: True
                color: 1, 1, 1, 1
            
            Button:
                text: '≡'
                size_hint_x: 0.2
                background_color: 0, 0, 0, 0
                on_press: root.open_menu()
        
        # Панель вкладок (как <nav>)
        TabbedPanel:
            do_default_tab: False
            tab_pos: 'top_mid'
            
            # Первая вкладка - Чаты
            TabbedPanelItem:
                text: 'Чаты'
                
                ScrollView:
                    GridLayout:
                        id: chat_list
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: '5dp'
                        padding: '10dp'
            
            # Вторая вкладка - Контакты  
            TabbedPanelItem:
                text: 'Контакты'
                
                ScrollView:
                    GridLayout:
                        id: contact_list
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: '2dp'
                        padding: '10dp'
            
            # Третья вкладка - Настройки
            TabbedPanelItem:
                text: 'Настройки'
                
                ScrollView:
                    GridLayout:
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        padding: '20dp'
                        spacing: '15dp'
                        
                        Label:
                            text: 'Настройки'
                            font_size: '20sp'
                            bold: True
                            size_hint_y: None
                            height: '40dp'
                        
                        # Переключатель (как <input type="checkbox">)
                        BoxLayout:
                            size_hint_y: None
                            height: '40dp'
                            Label:
                                text: 'Уведомления'
                            Switch:
                                id: notifications_switch
                                active: True
                        
                        # Поле ввода (кам <input type="text">)
                        BoxLayout:
                            size_hint_y: None
                            height: '40dp'
                            Label:
                                text: 'Имя:'
                            TextInput:
                                hint_text: 'Ваше имя'
                                id: name_input
                        
                        # Кнопка сохранения
                        Button:
                            text: 'Сохранить'
                            size_hint_y: None
                            height: '50dp'
                            background_color: 0.07, 0.47, 0.75, 1
                            color: 1, 1, 1, 1
                            on_press: root.save_settings()

# Стиль для карточек чатов (как CSS класс)
<ChatCard@Button>:
    size_hint_y: None
    height: '70dp'
    background_color: 0, 0, 0, 0
    background_normal: ''
    
    BoxLayout:
        padding: '10dp'
        spacing: '15dp'
        
        # Аватар (как <div class="avatar">)
        BoxLayout:
            size_hint_x: 0.2
            canvas.before:
                Color:
                    rgba: 0.8, 0.8, 0.8, 1
                Ellipse:
                    pos: self.pos
                    size: self.size
            Label:
                text: root.text[0].upper()
                font_size: '20sp'
                bold: True
        
        # Информация о чате
        BoxLayout:
            orientation: 'vertical'
            spacing: '5dp'
            
            Label:
                text: root.text
                font_size: '18sp'
                bold: True
                halign: 'left'
                text_size: self.width, None
            
            Label:
                text: 'Последнее сообщение...'
                font_size: '14sp'
                color: 0.5, 0.5, 0.5, 1
                halign: 'left'
                text_size: self.width, None
        
        # Время (как <span class="time">)
        Label:
            text: '12:30'
            font_size: '12sp'
            color: 0.5, 0.5, 0.5, 1
            size_hint_x: 0.2

# Стиль для контактов
<ContactCard@Button>:
    size_hint_y: None
    height: '60dp'
    background_color: 0, 0, 0, 0
    
    BoxLayout:
        padding: '10dp'
        
        # Статус онлайн
        BoxLayout:
            size_hint_x: 0.1
            canvas.before:
                Color:
                    rgba: 0.2, 0.8, 0.2, 1 if root.online else 0.5
                Ellipse:
                    pos: self.pos
                    size: self.size
        
        Label:
            text: root.text
            font_size: '18sp'
            halign: 'left'

# Стиль для сообщений
<MessageBubble@BoxLayout>:
    orientation: 'vertical'
    size_hint: (0.7, None) if root.is_my else (0.7, None)
    size_hint_x: None
    height: self.minimum_height
    padding: '10dp'
    
    canvas.before:
        Color:
            rgba: (0.07, 0.47, 0.75, 1) if root.is_my else (0.9, 0.9, 0.9, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20]
    
    Label:
        text: root.message_text
        font_size: '16sp'
        color: (1, 1, 1, 1) if root.is_my else (0, 0, 0, 1)
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
    
    Label:
        text: root.time
        font_size: '12sp'
        color: (1, 1, 1, 0.8) if root.is_my else (0.5, 0.5, 0.5, 1)
        halign: 'right'
        size_hint_x: 1
'''

# Загружаем наш "HTML" (KV код)
Builder.load_string(kv_code)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.load_data)
    
    def load_data(self, dt):
        # Загружаем чаты (как будто из API)
        chats = [
            'Анна Иванова',
            'Иван Петров', 
            'Рабочий чат',
            'Семья',
            'Друзья'
        ]
        
        # Добавляем чаты в список
        for chat in chats:
            card = ChatCard(text=chat)
            card.bind(on_press=lambda instance, name=chat: self.open_chat(name))
            self.ids.chat_list.add_widget(card)
        
        # Добавляем контакты
        contacts = [
            {'name': 'Мария', 'online': True},
            {'name': 'Сергей', 'online': False},
            {'name': 'Алексей', 'online': True},
        ]
        
        for contact in contacts:
            card = ContactCard(text=contact['name'])
            card.online = contact['online']
            self.ids.contact_list.add_widget(card)
    
    def open_chat(self, name):
        # Создаем экран чата
        chat_screen = ChatScreen(name=name)
        self.manager.add_widget(chat_screen)
        self.manager.current = 'chat'
    
    def open_menu(self):
        print("Открыть меню")
    
    def save_settings(self):
        name = self.ids.name_input.text
        notifications = self.ids.notifications_switch.active
        print(f"Сохранено: Имя={name}, Уведомления={notifications}")

class ChatScreen(Screen):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        
        # Создаем интерфейс чата
        layout = BoxLayout(orientation='vertical')
        
        # Шапка чата
        header = BoxLayout(size_hint_y=0.1)
        header.add_widget(Button(
            text='←',
            on_press=self.go_back,
            size_hint_x=0.2
        ))
        header.add_widget(Label(
            text=name,
            font_size='20sp',
            bold=True
        ))
        
        # История сообщений
        scroll = ScrollView()
        self.message_container = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing='10dp',
            padding='10dp'
        )
        self.message_container.bind(minimum_height=self.message_container.setter('height'))
        scroll.add_widget(self.message_container)
        
        # Поле ввода
        input_layout = BoxLayout(size_hint_y=0.15, padding='5dp')
        self.message_input = TextInput(
            hint_text='Введите сообщение...',
            multiline=False
        )
        send_btn = Button(
            text='➤',
            size_hint_x=0.2,
            on_press=self.send_message
        )
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(send_btn)
        
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(input_layout)
        
        self.add_widget(layout)
        
        # Загружаем историю
        self.load_messages()
    
    def load_messages(self):
        # Пример сообщений
        messages = [
            {'text': 'Привет! Как дела?', 'is_my': False, 'time': '12:30'},
            {'text': 'Всё отлично!', 'is_my': True, 'time': '12:31'},
            {'text': 'Встречаемся в 18:00', 'is_my': False, 'time': '12:32'},
        ]
        
        for msg in messages:
            bubble = MessageBubble()
            bubble.message_text = msg['text']
            bubble.is_my = msg['is_my']
            bubble.time = msg['time']
            self.message_container.add_widget(bubble)
    
    def send_message(self, instance):
        text = self.message_input.text.strip()
        if text:
            bubble = MessageBubble()
            bubble.message_text = text
            bubble.is_my = True
            bubble.time = time.strftime('%H:%M')
            self.message_container.add_widget(bubble)
            self.message_input.text = ''
    
    def go_back(self, instance):
        self.manager.current = 'main'

class TelegramApp(App):
    def build(self):
        Window.clearcolor = (0.96, 0.96, 0.96, 1)  # Telegram background
        
        # Менеджер экранов
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        
        return sm

# Файл для сборки APK (buildozer.spec) смотрим ниже
