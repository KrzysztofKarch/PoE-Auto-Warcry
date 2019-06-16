# PoE Auto Warcry
#
# author: Krzysztof Karch
# author mail: krzysztof.karch@wp.pl
#
# version 1.00 (14.06.2019)

import press_key
import threading
import tkinter as tk
from tkinter import Spinbox
from tkinter import scrolledtext
from tkinter import messagebox

BUTTON_FONT = 'Helvetica 9 bold'
STATE_FONT = 'Helvetica 18 bold'


class Application_Warcry(tk.LabelFrame):
    """
    A single application that allows automatic clicking keyboard key.
    Allows you to specified keyboard key and time delay.
    Contains all widgets it needs.
    Checks every change made by the user.
    Starts or stops automatic clicking.
    """
    def __init__(self, master, row, column, default_key,
                 default_delay, min_delay, max_delay):
        super(Application_Warcry, self).__init__(master, bd = 4)
        self.grid(row = row, column = column)

        self.is_running = False
        self.are_user_values_correct = True
        self.key = default_key
        self.delay = default_delay
        self.min_delay = min_delay
        self.max_delay = max_delay

        self.create_widgets()

    def create_widgets(self):
        description = 'Automatic key pressing after a fixed delay.\n\n'\
                    + 'Program will add some little random delay and works\n'\
                    + 'with 3 different scenarios to imitate real human.\n\n'\
                    + 'Created for Path of Exile instant warcies.\n'\
                    + 'Default setting for 20% increased Warcry Cooldown\n'\
                    + 'Recovery Speed. \n'
        tk.Label(self, text = description, wraplength = 300, justify=tk.LEFT)\
                .grid(row = 0, column = 0, columnspan = 2)

        self.label_state = tk.Label(self, text = 'OFF', font = STATE_FONT)
        self.label_state.grid(row = 0, column = 2)

        tk.Label(self, text = 'Delay [{} - {}s]'.format(str(self.min_delay),
                                                        str(self.max_delay)))\
                .grid(row = 1, column = 0)

        self.spinbox_delay_default = tk.DoubleVar(value = self.delay)
        self.spinbox_delay = Spinbox(self, from_ = int(self.min_delay),
                                    to = int(self.max_delay), increment = 0.01,
                                    textvariable = self.spinbox_delay_default)
        self.spinbox_delay.grid(row = 1, column = 1)
        # set tracing for each user change in self.spinbox_delay widget
        self.spinbox_delay_default.trace('w', self.check_spinbox_delay)

        delay_tips = 'Take your "Cooldown Time" from tooltip in game '\
                    + 'and add 0.1 due to latency in connection'
        tk.Label(self, text = delay_tips, wraplength = 150, justify = tk.CENTER)\
                .grid(row = 1, column = 2)

        tk.Label(self, text = 'Key')\
                .grid(row = 2, column = 0)

        self.entry_key_default = tk.StringVar(value = self.key)
        self.entry_key = tk.Entry(self, textvariable = self.entry_key_default)
        self.entry_key.grid(row = 2, column = 1)
        # set tracing for each user change in entry_key widget
        self.entry_key_default.trace('w', self.check_entry_key)

        key_tips = 'One char, small letter/digit\nExample: x'
        tk.Label(self, text = key_tips, wraplength = 150, justify = tk.CENTER)\
                .grid(row = 2, column = 2)

        self.button_stop = tk.Button(self, text = 'Stop Warcry',
                                    command = self.stop_pressing,
                                    font = BUTTON_FONT)
        self.button_stop.grid(row = 3, column = 0)

        self.button_start = tk.Button(self, text = 'Start Warcry',
                                    command = self.start_pressing,
                                    font = BUTTON_FONT)
        self.button_start.grid(row = 3, column = 1)

    def check_spinbox_delay(self, *ignoredArgs):
        """checking each user change made in spinbox_delay widget

        value should be convertible to float
        and in range [self.min_delay, self.max_delay]

        after each change self.button_start widget will be disabled,
        checked, and if correct enabled"""
        self.are_user_values_correct = False
        self.button_start['state'] = 'disabled'
        try:
            new = float(self.spinbox_delay.get())
            new = round(new, 2)
            if self.min_delay <= new <= self.max_delay:
                # if user's change is correct self.delay is setted
                # for user's value and button_start widget will be enabled
                self.delay = new
                self.are_user_values_correct = True
                self.button_start['state'] = 'normal'
                self.spinbox_delay['bg'] = 'white'
            else:
                raise ValueError
        except ValueError:
            self.spinbox_delay['bg'] = 'pink'

    def check_entry_key(self, *ignoredArgs):
        """checking each user change made in entry_key widget"""
        self.are_user_values_correct = False
        self.button_start['state'] = 'disabled'
        if len(self.entry_key.get()) == 1:
            self.key = self.entry_key.get()
            self.are_user_values_correct = True
            self.button_start['state'] = 'normal'
            self.entry_key['bg'] = 'white'
        else:
            self.entry_key['bg'] = 'pink'

    def press_the_key(self):
        """starts automatic clicking keyboard key specified in self.key"""
        while self.is_running:
            press_key.press_key(key = self.key, delay = self.delay)

    def start_pressing(self):
        """Actions after the user clicks the 'Start'."""
        if self.is_running == False and self.are_user_values_correct == True:
            self.is_running = True
            self.t = threading.Thread(target = self.press_the_key)
            self.t.start()

            self.label_state['text'] = 'ON'
            self.label_state['fg'] = 'red'
            self.button_start['state'] = 'disabled'
            self.spinbox_delay['state'] = 'disabled'
            self.entry_key['state'] = 'disabled'

    def stop_pressing(self):
        """Actions after the user clicks the 'Stop'."""
        if self.is_running == True:
            self.is_running = False
            def refresh():
                self.label_state['text'] = 'OFF'
                self.label_state['fg'] = 'black'
                self.button_start['state'] = 'normal'
                self.spinbox_delay['state'] = 'normal'
                self.entry_key['state'] = 'normal'

            # Prevents the user from starting a new thread with clicking
            # when the old thread is already working. Stopping takes time.
            time_to_refresh = int(self.delay * 1000)
            self.label_state['text'] = 'stopping'
            self.master.after(time_to_refresh, refresh)


class Application_Guard(Application_Warcry):
    """
    Modified Application for Guard skills.
    Difference only in the text of the widgets.
    """
    def create_widgets(self):
        description = 'You can use it also for Guard skills like:'\
                    + '                            \n'\
                    + 'Steelskin\n'\
                    + 'Molten Shell\n'

        tk.Label(self, text = description, wraplength = 300, justify=tk.LEFT)\
                .grid(row = 0, column = 0, columnspan = 2)

        self.label_state = tk.Label(self, text = 'OFF', font = 'Helvetica 18 bold')
        self.label_state.grid(row = 0, column = 2)

        tk.Label(self, text = 'Delay [{} - {}s]'.format(str(self.min_delay),
                                                        str(self.max_delay)))\
                .grid(row = 1, column = 0)

        self.spinbox_delay_default = tk.DoubleVar(value = self.delay)
        self.spinbox_delay = Spinbox(self, from_ = int(self.min_delay),
                                    to = int(self.max_delay), increment = 0.01,
                                    textvariable = self.spinbox_delay_default)
        self.spinbox_delay.grid(row = 1, column = 1)
        # set tracing for user time delay changes
        self.spinbox_delay_default.trace('w', self.check_spinbox_delay)

        delay_tips = 'Sum Duration Time, Cooldown Time\n'\
                    + 'and add 0.1 due to latency in connection'
        tk.Label(self, text = delay_tips, wraplength = 150, justify = tk.CENTER)\
                .grid(row = 1, column = 2)

        tk.Label(self, text = 'Key')\
                .grid(row = 2, column = 0)

        self.entry_key_default = tk.StringVar(value = self.key)
        self.entry_key = tk.Entry(self, textvariable = self.entry_key_default)
        self.entry_key.grid(row = 2, column = 1)
        # set tracing for user key changes
        self.entry_key_default.trace('w', self.check_entry_key)

        key_tips = 'One char, small letter/digit\nExample: x'
        tk.Label(self, text = key_tips, wraplength = 150, justify = tk.CENTER)\
                .grid(row = 2, column = 2)

        self.button_stop = tk.Button(self, text = 'Stop Guard',
                                    command = self.stop_pressing,
                                    font = BUTTON_FONT)
        self.button_stop.grid(row = 3, column = 0)

        self.button_start = tk.Button(self, text = 'Start Guard',
                                    command = self.start_pressing,
                                    font = BUTTON_FONT)
        self.button_start.grid(row = 3, column = 1)


class Manager(tk.Frame):
    """
    Class created for managing Applications, stores reference to them
    in list self.apps, can start and stop all Applications.
    """
    def __init__(self, master, row, column, applications):
        super(Manager, self).__init__(master)
        self.apps = applications
        self.grid(row = row, column = column)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text = '\nTest:')\
            .grid(row = 0, column = 0, sticky = tk.W)

        self.scrolledtext_test = scrolledtext.ScrolledText(self, width = 45,
                                                            height = 3)
        self.scrolledtext_test.grid(row = 1, column = 0, columnspan = 2,
                                    sticky = tk.W, pady = 15)

        self.button_clear = tk.Button(self, text = 'Clear',
                                    command = self.clear_entry_test)
        self.button_clear.grid(row = 1, column = 2, sticky = tk.W)

        self.button_stop_all = tk.Button(self, text = 'Stop Warcry + Guard',
                                        command = self.stop_all, font = BUTTON_FONT)
        self.button_stop_all.grid(row = 2, column = 0)

        self.button_start_all = tk.Button(self, text = 'Start Warcry + Guard',
                                        command = self.start_all, font = BUTTON_FONT)
        self.button_start_all.grid(row = 2, column = 1)
        self.button_start_all.focus()

    def clear_entry_test(self):
        self.scrolledtext_test.delete(0.0, tk.END)

    def start_all(self):
        self.button_start_all['state'] = 'disabled'
        self.button_stop_all.focus()
        for app in self.apps:
            app.start_pressing()

    def stop_all(self):
        # disable self.button_start_all to prevent starting
        # Applications when they are stopping
        self.button_start_all['state'] = 'disabled'

        # activate self.button_start_all after
        # the longest delay time chosen from all running Applications
        time_to_refresh = [0.001]
        for app in self.apps:
            if app.is_running == True:
                time_to_refresh.append(app.delay)
        time_to_refresh = int(max(time_to_refresh) * 1000) # conversion to ms

        def refresh():
            self.button_start_all['state'] = 'normal'
            self.button_start_all.focus()

        self.master.after(time_to_refresh, refresh)
        # when time_to_refresh is setted,
        # start stopping all Applications
        for app in self.apps:
            app.stop_pressing()


def create_menu(master, manager):
    """Creates menu with just 2 options: Exit and About. """
    def _quit():
        manager.stop_all()
        master.quit()
        master.destroy()
        exit()

    def _about():
        text = 'PoE Automatic Warcry\n\n' \
             + 'Author:\n\tKrzysztof Karch\n' \
             + '\tkrzysztof.karch@wp.pl\n\n' \
             + 'Licence: \n\tGNU General Public License'
        messagebox.showinfo('info', text)

    # creating Menu object for menu bar
    menu_bar = tk.Menu(master)
    master.configure(menu = menu_bar)
    # create 'File' menu and assign it to menu_bar
    file = tk.Menu(menu_bar, tearoff = 0) # tearoff prevent pulling menu down
    # Add item to 'File' menu
    file.add_command(label = 'Exit', command = _quit)

    # create 'Info' menu and assign it to menu_bar
    info = tk.Menu(menu_bar, tearoff = 0)
    # Add item to 'Info' menu
    info.add_command(label = 'about', command = _about)

    # add_cascade will makes menu visible
    menu_bar.add_cascade(label = 'File', menu = file)
    menu_bar.add_cascade(label = 'Info', menu = info)


def main():
    root = tk.Tk()
    root.geometry('450x640')
    root.title('PoE Auto Warcry')

    app = Application_Warcry(
        master = root, row = 0, column = 0, default_key = 'r',
        default_delay = 3.43, min_delay = 1.0, max_delay = 10.0
        )

    app2 = Application_Guard(
        master = root, row = 1, column = 0, default_key = 't',
        default_delay = 4.6, min_delay = 1.0, max_delay = 20.0
        )

    apps = [app, app2]

    manager = Manager(
        master = root, row = 2, column = 0, applications = apps
        )

    create_menu(root, manager)

    def on_exit():
        """stop pressing keys"""
        manager.stop_all()
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_exit) # overwrites closing by X
    root.mainloop()

if __name__ == '__main__':
    main()
