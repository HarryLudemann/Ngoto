
import os
import sys
import time
from subprocess import Popen
import threading


# this is not called on the main thread!
def handle_activated(sender, _):
    path = os.path.expanduser("~\\Documents")
    Popen('explorer ' + path)


def notify(title, message, button_name=None):
    """ Send a windows notification"""
    import winsdk.windows.ui.notifications as notifications
    import winsdk.windows.data.xml.dom as dom
    # define your notification as
    if button_name:
        tString = f"""
    <toast duration="short">
        <visual>
            <binding template='ToastGeneric'>
                <text>{title}</text>
                <text>{message}</text>
            </binding>
        </visual>

        <actions>
            <action
                content="{button_name}"
                arguments=""
                activationType="foreground"/>
        </actions>
    </toast>
    """
    else:
        tString = f"""
    <toast duration="short">
        <visual>
            <binding template='ToastGeneric'>
                <text>{title}</text>
                <text>{message}</text>
            </binding>
        </visual>
    </toast>
    """

    # convert notification to an XmlDocument
    xDoc = dom.XmlDocument()
    xDoc.load_xml(tString)
    notification = notifications.ToastNotification(xDoc)

    # add the activation token.
    if button_name:
        notification.add_activated(handle_activated)

    # create notifier
    nManager = notifications.ToastNotificationManager
    # link it to your Python executable (or whatever you want I guess?)
    notifier = nManager.create_toast_notifier(sys.executable)

    # display notification
    notifier.show(notification)
    duration = 7  # "short" duration for Toast notifications

    # We have to wait for the results from the notification
    # If we don't, the program will just continue and maybe
    # even end before a button is clicked
    thread = threading.Thread(target=lambda: time.sleep(duration))
    thread.start()


if __name__ == "__main__":
    notify("Hello", "World", "Click me")
