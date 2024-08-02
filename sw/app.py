import pyxel
import PyxelUniversalFont as puf
from pygame import mixer

import json
import time

from params import Params
from serial_device import SerialDevice

SCENE_TITLE:int = 0
SCENE_PLAY:int = 1


class App:
    def __init__(self):
        self.scene:int  = SCENE_TITLE
        self.params:params.params.Params = Params()
        self.device:serial_device.serial_device.SerialDevice = SerialDevice()
        self.is_device_connect:bool = self.device.check_port()
        self.is_start:bool = False
        self.data = {}
        self.start_time:float = 0
        self.end_time:float  = 0
        self.crr_time:float = 0
        self.elps_time:float = 0

        mixer.init()
        self.title_se_play:bool = False

        pyxel.init(1016, 762, title="指振りどんだけ〜！！コンボゲーム")
        self.writer:PyxelUniversalFont.src.root.Writer = puf.Writer("misaki_gothic.ttf")
        pyxel.run(self.update, self.draw)


    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            self.device.send_data('F')
            pyxel.quit()

        if self.params.pos_title_y < 222:
            self.params.pos_title_y += 6
        elif self.params.pos_title_y > 221 and self.title_se_play is False:
            mixer.music.load('./audio/dondakee.mp3')
            mixer.music.play(1)
            self.title_se_play = True

        self.is_device_connect = self.device.check_port()
        if self.is_device_connect:
            if pyxel.btn(pyxel.KEY_SPACE) and self.is_start is False:
                self.device.send_data('T')
                self.is_start = True
                self.scene = SCENE_PLAY
                self.elps_time:float = 0
                self.start_time = time.time()
            if self.is_start:
                self.data = self.device.get_data()
                self.crr_time = time.time()
                self.elps_time = self.crr_time - self.start_time
                if 'is_start' in self.data:
                    if self.data['is_start'] == 'false':
                        mixer.music.stop()
                        mixer.music.load('./audio/seoinagee.mp3')
                        mixer.music.play(1)
                        self.is_start = False
                        self.start_time:float = 0
                        self.end_time:float  = 0
                        self.crr_time:float = 0
                else:
                    self.select_se(int(self.data['dondakeeState']), int(self.data['dondakeCnt']))


    def draw(self) -> None:
        pyxel.cls(0)

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()


    def elps_time_str(self, sec:float) -> str:
        sec = round(sec)
        h = sec // 3600
        m = (sec -h * 3600) // 60
        s = sec - h * 3600 - m * 60

        return f'{m:02}:{s:02}'


    def draw_dondakee(self, dondakee_state:int) -> None:
        if dondakee_state == 2:
            self.writer.draw(398, 450, 'ドンダケ〜', 100, 7)



    def draw_title_scene(self) -> None:
        if self.params.pos_title_y >= 222:
            self.writer.draw(38, 222, "指振りどんだけ〜！！コンボゲーム", 60, pyxel.frame_count % 16)
            if self.is_device_connect:
                self.writer.draw(428, 450, "Press Space", 30, 7)
            else:
                self.writer.draw(330, 450, "Please Connect a Device", 30, 7)
        else:
            self.writer.draw(38, self.params.pos_title_y, "指振りどんだけ〜！！コンボゲーム", 60, 7)


    def draw_play_scene(self) -> None:
        self.writer.draw(398, 250, self.elps_time_str(self.elps_time), 100, 7)
        #self.draw_dondakee(int(self.data['dondakeeCnt']))
        #self.writer.draw(10, 450, json.dumps(self.data), 20, 7)
        if self.is_start is False:
            if self.is_device_connect:
                self.writer.draw(428, 450, "Press Space", 30, 7)
            else:
                self.writer.draw(330, 450, "Please Connect a Device", 30, 7)


    def select_se(self, dondakee_state:int, dondakee_cnt:int) -> None:
        if dondakee_state == 1:
            mixer.music.load('./audio/matsu_dondakee.mp3')
            mixer.music.play(1)
        elif dondakee_state == 2 and dondakee_cnt < 3:
            mixer.music.load('./audio/dondakee.mp3')
            mixer.music.play(1)
        elif dondakee_state == 2 and dondakee_cnt > 2:
            mixer.music.load('./audio/dondakedondakedondakee.mp3')
            mixer.music.play(1)
        elif dondakee_state == 3:
            mixer.music.stop()
            mixer.music.load('./audio/seoinagee.mp3')
            mixer.music.play(1)


if __name__ == '__main__':
    App()
