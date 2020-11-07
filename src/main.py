from kivy.lang import Builder
from kivymd.app import MDApp
# from kivy.core.window import Window
# from kivy.properties import BooleanProperty
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from plyer import stt
import logging
stt.prefer_offline = False
# from kivy.uix.screenmanager import ScreenManager, Screen
## primary_dark

KV = '''
GridLayout:
    cols:1
    MDToolbar:
        title: "S2TAPP"
        anchor_title: 'center'
        elevation: 8
        left_action_items: [["hamburger", lambda x:'']]
        right_action_items:[["settings", lambda x:'']]
    FloatLayout:
        MDFloatingActionButton:
            icon: "microphone"
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {'center_x': 0.30, 'center_y':0.60}
            elevation_normal: 10
            on_press:app.voice_command()
        MDFloatingActionButton:
            icon: "keyboard"
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {'center_x': 0.65, 'center_y':0.60}
            elevation_normal: 10
            on_press:app.show_alert_dialog_port()
            '''

# class TogglePage(Screen):
#     pass

# class SettingsPage(Screen):
#     pass

class Test(MDApp):
    def build(self):
        self.a=False
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.RECORD_AUDIO,Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE])
        return Builder.load_string(KV)

    def voice_command(self):
        if(self.a==True):
            self.a=False
        else:
            self.a=True

        if(stt.exist()):
            if(self.a==True):   
              toast("listening speak")
              stt.start()
            elif(self.a==False):
             if(stt.listening==True):
              toast("stopped listening")#remove this wait till little
              stt.stop()
              self.result=stt.results
              logging.info(self.result)
              self.show_recognized_text()

        else:
            toast("your device doesnot support speech to text")

    def show_alert_dialog_port(self): 
            print("i entered")      
            self.dialog = MDDialog(
                type="custom",
                content_cls=MDTextField(mode= "rectangle"),
                buttons=[
                    MDFlatButton(
                        text="Ok", text_color=self.theme_cls.primary_color,on_press=self.get_cmd
                    ),
                    MDFlatButton(
                        text="Cancel", text_color=self.theme_cls.primary_color,on_press=self.dialog_close
                    ),
                ],
                size_hint=(0.9,1)
            )
           
            self.dialog.content_cls.hint_text=str("Enter command")
            
            self.dialog.open()

    def show_recognized_text(self):
     try:
        if(self.result[0]):
            logging.info("showing dialog box")
            self.dialog = MDDialog(
                type="custom",
                text=str(self.result[0]),
                buttons=[
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color,on_press=self.dialog_close
                    ),
                ],
                size_hint=(0.9,1)
            )
            
            self.dialog.open()
     except IndexError:
         toast("too quick wait for beep to end,try again")

    
    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)
    def get_cmd(self,g):
        print(self.dialog.content_cls.text)
        self.dialog.content_cls.text=""
        





if __name__ == "__main__":
   Test().run()