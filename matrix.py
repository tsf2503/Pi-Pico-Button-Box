import board
import digitalio
import usb_hid
import time


class ButtonMatrix:
    
    def __init__(self, col_pins, row_pins, switch_col_pins, switch_row_pins):
        #Initialize the buttons 
        self.cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
        self.rows = [digitalio.DigitalInOut(pin) for pin in row_pins]

        #Initialize the rows
        self.switch_rows = [digitalio.DigitalInOut(pin) for pin in switch_row_pins]
        #List to hold switch columns (filled in column set loop) 
        # self.switch_cols = []
        #List holds the status of each switch
        self.switch_status = [0] * len(switch_col_pins) * 2
        
        #Set columns as Output
        for i, col in enumerate(self.cols):
            col.direction = digitalio.Direction.OUTPUT
            #checks if the current col has switches if so copies the col to the switch list
            # if i in switch_col_pins:
            #     self.switch_cols.append(col)
        self.switch_cols = self.cols
        #Set rows as Input pull down
        for row in self.rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN
        for row in self.switch_rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN


    def Check(self):
        for col_num, col in enumerate(self.cols):
            col.value = 1
            for row_num, row in enumerate(self.rows):
                if row.value != 1: continue

                if col_num == 6:
                    button_num = 30 + row_num
                else:
                    button_num = (row_num + 2)* 5 + col_num + 1
                col.value = 0
                return button_num
            col.value = 0

    def SwitchCheck(self):
        for col_num, col in enumerate(self.switch_cols):
            if col_num == 5: continue
            col.value = 1
            # print(col_num)
            for row_num, row in enumerate(self.switch_rows):
                # time.sleep(1)
                button_num = row_num * 5 + col_num + 1
                # print(row_num, row.value, self.switch_status,)
                if row.value == self.switch_status[button_num - 1]: continue
                self.switch_status[button_num - 1] = row.value
                if row.value == 1:
                    self.PressButton(button_num)
                else:
                    self.ReleaseButton(button_num)
            col.value = 0

    def ClickButton(self, button):
        print(f"Click Button; {button}")
    
    def PressButton(self, button):
        print(f"Press Button; {button}")

    def ReleaseButton(self, button):
        print(f"Release Button; {button}")

