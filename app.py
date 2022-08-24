"""This is the main file for running inforBilling. This app uses selenium to open infor
    and run a script that will finish billing for orders given.
"""


import os

import PySimpleGUI as sg
from billSelenium import billingOrders
# from Utils import csvUtils


def setUpGui() -> sg.Window:
    """This sets up the GUI which where the csv file, and login info will be entered.

    Returns:
        window: selenium window
    """

    # Add a touch of color DarkBlue3 or Default
    sg.theme('DefaultNoMoreNagging')
    # All the stuff inside your window.

    layout = [
        # [sg.Titlebar(title='Order Automation')],
        [sg.Push(), sg.Text('Enter your infor Login!'), sg.Push()],
        [sg.Push(), sg.Text('BILLING: Version 1.3'), sg.Push()],
        [sg.Push(), sg.Text('', key="-Update-", text_color="red"), sg.Push()],
        [sg.Text('Username:'), sg.InputText(key="-Username-")],
        [sg.Text('Password:'), sg.InputText(key="-Password-")],
        [sg.Push(), sg.Text('Import the CSV file from Shopify'), sg.Push()],
        [sg.Push(), sg.Input(enable_events=True, size=(18, 1)),
            sg.FileBrowse(key="-File-"), sg.Push()],
        [sg.Push(), sg.Button('Ok'), sg.Button('Cancel')],
        [sg.Push(), sg.Text('', key="-Failed-", text_color="red"), sg.Push()],
        [sg.Push(), sg.Text('', key="-Finished-", text_color="green"), sg.Push()],
        [sg.Push(), sg.Button('Export Failed Orders', key='-Export-'), sg.Push()],
    ]

    # Create the Window
    window = sg.Window('Billing Automation', layout, resizable=True)
    return window


def main():
    # This starts up the GUI and returns the window and runs a while loop until the GUI is closed
    window = setUpGui()
    while True:

        # These hold the variables inside the GUI
        event, values = window.read()

        # The Ok Button will trigger the selenium functions for billing.
        if event == 'Ok':
            billingOrders.login(values["-Username-"], values["-Password-"])

            billingOrders.customerSetUp()

        if event in (sg.WIN_CLOSED, 'Cancel'):  # if user closes window or clicks cancel
            try:
                billingOrders.closeWeb()
            except Exception:
                print("not closed properly..doesn't matter")
            break

    window.close()


if __name__ == "__main__":
    main()
