from elements import *
import Saving_Dialog as save
import wx


class WorkWindow(wx.Frame):
    text_box: wx.TextCtrl
    message_box: wx.TextCtrl
    submit_button: wx.Button
    saving_button: wx.Button

    def __init__(self):
        super().__init__(
            None,
            title='Football Manager',
            size=wx.Size(350, 400)
        )
        self.build_widgets()
        self.build_handlers()
        self.main_message_for_searching = ''
        self.keeping = save.Queue()

    def build_widgets(self):
        panel = wx.BoxSizer(wx.VERTICAL)  # для расстановки компонентов

        self.text_box = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.message_box = wx.TextCtrl(self, size=wx.Size(40, 30))
        self.submit_button = wx.Button(self, label='Send Message')
        self.saving_button = wx.Button(self, label='Save Dialog')
        self.message_box.SetFocus()

        panel.Add(self.text_box, wx.SizerFlags(1).Expand())
        panel.Add(self.message_box, wx.SizerFlags(0).Expand().Border(wx.BOTTOM | wx.UP, 5))
        panel.Add(self.submit_button, wx.SizerFlags(0).Expand())
        panel.Add(self.saving_button, wx.SizerFlags(0).Expand())

        self.SetSizer(panel)

    def build_handlers(self):
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.submit_button.Bind(wx.EVT_KEY_DOWN, self.press_enter)
        self.saving_button.Bind(wx.EVT_BUTTON, self.keep_data)

        self.message_box.Bind(wx.EVT_TEXT_ENTER, self.press_enter)

    def type_text(self, event):
        key_code = event.GetKeyCode()
        if key_code == ENTER_KEY:
            self.message_box.Bind(wx.EVT_KEY_DOWN, self.press_enter)
        else:
            self.message_box.Unbind(wx.EVT_KEY_DOWN)

    def keep_data(self, event):  # сохранение данных в файл
        save.saving_on_file(self.keeping)
        self.text_box.AppendText(SYS+" Данные были сохранены\n")

    def press_enter(self, event):  # обработка ввода данных при нажатии на ENTER
        self.on_button_click(event)
        event.Skip()

    def on_button_click(self, event):
        message = self.message_box.GetValue()
        if message != '':
            if greeting(message) is not False:
                self.text_box.AppendText(f'{USER+message}\n')
                self.keeping.push(f'{USER+message}\n')
                self.text_box.AppendText(f'{SYS+greeting(message)}\n')
                self.keeping.push(f'{SYS+greeting(message)}\n')
            elif take_info_match(message) is not False:
                self.text_box.AppendText(f'{USER + message}\n')
                self.keeping.push(f'{USER + message}\n')
                self.text_box.AppendText(f'{SYS + take_info_match(message)}\n')
                self.keeping.push(f'{SYS + take_info_match(message)}\n')
            elif take_basic_answers(message) is not False:
                self.text_box.AppendText(f'{USER+message}\n')
                self.keeping.push(f'{USER + message}\n')
                self.text_box.AppendText(f'{SYS+take_basic_answers(message)}\n')
                self.keeping.push(f'{SYS+take_basic_answers(message)}\n')
            elif take_definition_answer(message) is not False:
                self.text_box.AppendText(f'{USER + message}\n')
                self.keeping.push(f'{USER + message}\n')
                self.text_box.AppendText(f'{SYS + take_definition_answer(message)}\n')
                self.keeping.push(f'{SYS + take_definition_answer(message)}\n')
            elif (message.lower() not in agreements) and (message.lower() not in renouncement):
                self.text_box.AppendText(f'{USER + message}\n')
                self.keeping.push(f'{USER + message}\n')
                self.text_box.AppendText(f'{SYS + google_answers[r.randint(0, len(google_answers)-1)]}\n')
                self.keeping.push(f'{SYS + google_answers[r.randint(0, len(google_answers)-1)]}\n')
                self.main_message_for_searching = message
            elif (message.lower() in agreements) and (self.main_message_for_searching != ''):
                self.text_box.AppendText(f'{USER + message}\n')
                self.keeping.push(f'{USER + message}\n')
                self.text_box.AppendText(f'{SYS + google_results[r.randint(0, len(google_results)-1)]}\n')
                self.keeping.push(f'{SYS + google_results[r.randint(0, len(google_results)-1)]}\n')
                googling(self.main_message_for_searching)
                self.main_message_for_searching = ''
            elif message.lower() in renouncement:
                self.text_box.AppendText(f'{USER + message}\n')
                self.keeping.push(f'{USER + message}\n')
                self.text_box.AppendText(f'{SYS + stop_searching}\n')
                self.keeping.push(f'{SYS + stop_searching}\n')
            else:
                self.text_box.AppendText(f'{USER + message}\n')
                self.keeping.push(f'{USER + message}\n')
                self.text_box.AppendText(f'{SYS + regrets[r.randint(0, len(regrets)-1)]}\n')
                self.keeping.push(f'{SYS + regrets[r.randint(0, len(regrets)-1)]}\n')
            self.message_box.SetValue('')
        else:
            self.text_box.AppendText(f'{ERROR_SYS}\n')
            self.keeping.push(f'{ERROR_SYS}\n')

    def set_greeting(self, text):
        self.text_box.AppendText(f'{SYS + text}\n')


if __name__ == '__main__':
    app = wx.App()
    window = WorkWindow()
    window.SetIcon(wx.Icon('image.ico'))
    window.Center()
    window.Show()
    window.set_greeting(greeting_system[r.randint(0, len(greeting_system)-1)])
    app.MainLoop()
