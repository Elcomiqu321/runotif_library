import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) 

# import module
from runotif.notif import popup_notif, toast_notif

def test_popup_notif():
    @popup_notif
    def sample_function():
        print('Started running...\n**')
        time.sleep(1)
        print('doing some stuff..\n**')
        time.sleep(1)
        print('Finished running...')

        return 'output value'
    
    op = sample_function()
    print(op)

def test_toast_windows():
    @toast_notif
    def sample_function():
        print('Started running...\n**')
        time.sleep(1)
        print('doing some stuff..\n**')
        time.sleep(1)
        print('Finished running...')

        return 'output value'
    
    op = sample_function()
    print(op)


if __name__ == '__main__':
    # test_popup_notif()
    # test_toast_windows()

    toast_notif()

    0