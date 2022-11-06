import cv2
import tkinter as tk

from KeyConfig import PokeKeycon
from LineNotify import Line_Notify
from logging import getLogger, DEBUG, NullHandler


class PokeController_Menubar(tk.Menu):
    def __init__(self, master, **kw):
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.master = master
        self.root = self.master.root
        self.ser = self.master.ser
        self.preview = self.master.preview
        self.show_size_cb = self.master.show_size_cb
        self.keyboard = self.master.keyboard
        self.settings = self.master.settings
        self.camera = self.master.camera
        self.poke_treeview = None
        self.key_config = None
        self.line = None

        tk.Menu.__init__(self, self.root, **kw)
        self.menu = tk.Menu(self, tearoff='false')
        self.menu_command = tk.Menu(self, tearoff='false')
        self.add(tk.CASCADE, menu=self.menu, label='メニュー')
        self.menu.add(tk.CASCADE, menu=self.menu_command, label='コマンド')

        self.menu.add('separator')
        self.menu.add('command', label='設定(dummy)')
        # TODO: setup command_id_arg 'false' for menuitem.
        self.menu.add('command', command=self.exit, label='終了')

        self.AssignMenuCommand()
        self.LineTokenSetting()

    # TODO: setup command_id_arg 'false' for menuitem.

    def AssignMenuCommand(self):
        self._logger.debug("Assigning menu command")
        self.menu_command.add('command', command=self.LineTokenSetting, label='LINE Token Check')
        # TODO: setup command_id_arg 'false' for menuitem.
        self.menu_command.add('command', command=self.OpenPokeHomeCoop, label='Pokemon Home 連携')
        self.menu_command.add('command', command=self.OpenKeyConfig, label='キーコンフィグ')
        self.menu_command.add('command', command=self.ResetWindowSize, label='画面サイズのリセット')

    # TODO: setup command_id_arg 'false' for menuitem.

    def OpenPokeHomeCoop(self):
        self._logger.debug("Open Pokemon home cooperate window")
        if self.poke_treeview is not None:
            self.poke_treeview.focus_force()
            return

        window2 = GetFromHomeGUI(self.root, self.settings.season, self.settings.is_SingleBattle)
        window2.protocol("WM_DELETE_WINDOW", self.closingGetFromHome)
        self.poke_treeview = window2

    def closingGetFromHome(self):
        self._logger.debug("Close Pokemon home cooperate window")
        self.poke_treeview.destroy()
        self.poke_treeview = None

    def LineTokenSetting(self):
        self._logger.debug("Show line API")
        if self.line is None:
            self.line = Line_Notify(self.camera)
        print(self.line)
        self.line.getRateLimit()
        # LINE.send_text_n_image("CAPTURE")

    def OpenKeyConfig(self):
        self._logger.debug("Open KeyConfig window")
        if self.key_config is not None:
            self.key_config.focus_force()
            return

        kc_window = PokeKeycon(self.root)
        kc_window.protocol("WM_DELETE_WINDOW", self.closingKeyConfig)
        self.key_config = kc_window

    def closingKeyConfig(self):
        self._logger.debug("Close KeyConfig window")
        self.key_config.destroy()
        self.key_config = None

    def ResetWindowSize(self):
        self._logger.debug("Reset window size")
        self.preview.setShowsize(360, 640)
        self.show_size_cb.current(0)

    def exit(self):
        self._logger.debug("Close Menubar")
        if self.ser.isOpened():
            self.ser.closeSerial()
            print("serial disconnected")

        # stop listening to keyboard events
        if self.keyboard is not None:
            self.keyboard.stop()
            self.keyboard = None

        # save settings
        self.settings.save()

        self.camera.destroy()
        cv2.destroyAllWindows()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    widget = PokeController_Menubar(root)
    widget.pack(expand=True, fill='both')
    root.mainloop()
