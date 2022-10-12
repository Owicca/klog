import os, time, math
import threading, random

from keys import ascii_keys, special, pressed

class BgWriter(threading.Thread):
    f = None
    tm = None
    time_delta = None
    end = False

    def __init__(self, f, tm, time_delta):
        super(BgWriter, self).__init__()
        #print("self started")

        self.f = f
        self.tm = tm
        self.time_delta = time_delta

    def __del__(self):
        #print("self terminate")
        self.terminate()
        #print("terminated")

        return

    def run(self, *args, **kwargs):
        while True:
            if self.end:
                #print("end run")
                break
            #print(f"iterate")
            new_tm = math.floor(time.time())
            if (new_tm - self.tm) > self.time_delta:
                self.tm = new_tm
                tpl = f'"{os.linesep}{self.tm},"'
                self.f.write(tpl)
            time.sleep(1)


class Writer(object):
    li = None
    f = None
    is_newline = False
    is_whitespace = False
    is_ascii = False
    is_upper = False
    bg_jobs = []

    def __init__(self, li, f):
        self.li = li
        self.f = f

    def __del__(self):
        for jb in self.bg_jobs:
            jb.end = True
            #print("singnal ending")
            jb.join()
            #print("joined")

    def get_metadata(self, ev):
        v = ev.get_keyboard_event()
        key_name = v.get_key().name
        s = v.get_key_state().name

        return [v, key_name, s]

    def set_upper(self, cur_s, new_s, key):
        """
        upper:
            - shift_pressed + letter
            - caps_pressed, one or more buttons pressed
        lower:
            - one or more buttons pressed
            - caps_pressed, one or more buttons pressed
            - caps_pressed, shift_pressed, one or more buttons pressed
            - shift_released, one or more buttons pressed
        """
        result = False
        is_shift = key in [special.left_shift, special.right_shift]
        is_caps = key in [special.capslock]

        if not is_shift and not is_caps:
            result = cur_s
            return result

        shift_on = is_shift and new_s == pressed

        result = shift_on

        return result

    def run(self, time_delta):
        """
        Iterate through events, format keyboard ones and write them
        """
        last = math.floor(time.time())
        delta = time_delta

        self.bg_jobs.append(BgWriter(self.f, last, delta))
        for jb in self.bg_jobs:
            jb.start()

        for ev in self.li.get_event():
            self.is_newline = False
            self.is_ascii = False
            if ev.type != 300:
                continue

            v, key_name, s = self.get_metadata(ev)

            parts = key_name.split("_")
            key = "unk"
            if len(parts) > 1:
                key = parts[1]

            self.is_upper = self.set_upper(self.is_upper, s, key_name)
            self.is_ascii = key in ascii_keys

            if not key in ascii_keys:
                key = f'[{key}]'

            if key_name == special.enter:
                key = os.linesep
                self.is_newline = True
            elif key_name in [special.space, special.tab]:
                key = " "
                self.is_whitespace = True

            if self.is_ascii and s == pressed:
                continue

            if not self.is_upper:
                key = key.lower()
            tpl = f'{key}'
            tm = last

            if self.is_newline:
                new_tm = math.floor(time.time())
                if (new_tm - tm) > delta:
                    last = tm = new_tm
                    tpl = f'"{key}{tm},"'
                else:
                    tpl = f'{key}'

            self.f.write(tpl)
