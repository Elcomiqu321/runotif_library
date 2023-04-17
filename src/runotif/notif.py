import os
import subprocess
import ctypes
import time
import traceback

def get_system():
    if os.name == 'posix':
        if 'darwin' in os.uname().sysname.lower(): return 'mac'
        else: return 'linux'
    elif os.name == 'nt': return 'windows'
    else: return 'unknown'

if get_system() == 'windows':
    try:
        import winrt.windows.ui.notifications as notifications
        import winrt.windows.data.xml.dom as dom
    except Exception as e:
        import winsdk.windows.ui.notifications as notifications
        import winsdk.windows.data.xml.dom as dom


def get_system():
    if os.name == 'posix':
        if 'darwin' in os.uname().sysname.lower(): return 'mac'
        else: return 'linux'
    elif os.name == 'nt': return 'windows'
    else: return 'unknown'

def windows_popup(message: str=None, title: str=None):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x0)

def windows_toast(message: str=None, title: str=None):
    app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe'

    #create notifier
    nManager = notifications.ToastNotificationManager
    notifier = nManager.create_toast_notifier(app)

    #define your notification as string
    tString = f"""
    <toast>
        <visual>
        <binding template='ToastGeneric'>
            <text>{title}</text>
            <text>{message}</text>
        </binding>
        </visual>
        <actions>
        <action
            content="Delete"
            arguments="action=delete"/>
        <action
            content="Dismiss"
            arguments="action=dismiss"/>
        </actions>    
    </toast>
    """

    #convert notification to an XmlDocument
    xDoc = dom.XmlDocument()
    xDoc.load_xml(tString)

    #display notification
    notifier.show(notifications.ToastNotification(xDoc))

def mac_linux_popup(message: str=None, title: str=None):
    os.system(f'notify-send "{title}" "{message}"')

def mac_linux_toast(message: str=None, title: str=None):
    os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')


def execution_status(func=None):
    start_time = time.time()
    failed = None
    try:
        if func is not None: returnValue = func()
        else: returnValue = None
    except Exception as e:
        print(e)
        traceback.print_exc()
        failed = True
    end_time = time.time()
    
    if func is not None:
        elapsed_time = f'{end_time - start_time:.2f}s'
        function_name = f'{func.__name__}() '
    else:
        elapsed_time, function_name = '', ''

    if failed: message = f'{function_name}execution failed\n {elapsed_time}'
    else: message = f'{function_name}execution successful\n {elapsed_time}'
    return message, returnValue

def popup_notif(func=None):
    def wrapper():
        message, returnValue = execution_status(func)
        title = 'Execution Notification'

        if get_system() == 'windows': windows_popup(message=message, title=title)
        elif get_system() in ['mac', 'linux']: mac_linux_popup(message=message, title=title)
        return returnValue
        
    if func is None: wrapper()
    else: return wrapper

def toast_notif(func=None):
    def wrapper():
        message, returnValue = execution_status(func)
        title = 'Execution Notification'

        if get_system() == 'windows': windows_toast(message=message, title=title)
        elif get_system() in ['mac', 'linux']: mac_linux_toast(message=message, title=title)
        return returnValue
    
    if func is None: wrapper()
    else: return wrapper

