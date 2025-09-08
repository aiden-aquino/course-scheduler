"""Graphical interface to the Advising Buddy application.

Author: CS149 Faculty
Version: 11/15/2023
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import schedule_utils
import catalog_utils

OPTIONS = [""]


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("JMU Advising Buddy")
        self.geometry("850x310")
        self.resizable(True, True)
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu = filemenu
        filemenu.add_command(label="Select Catalog JSON...", command=self.open_catalog)
        filemenu.add_command(
            label="Load Schedule JSON...", command=self.load_schedule, state=tk.DISABLED
        )
        filemenu.add_command(
            label="Save Schedule JSON...", command=self.save_schedule, state=tk.DISABLED
        )
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10)

        # Add a separate frame for the labels and fields
        course_info_frame = ttk.Frame(main_frame)
        course_info_frame.grid(
            row=0, column=0, columnspan=8, padx=10, pady=5, sticky=tk.W
        )
        self.option_variables = dict()
        self.option_menus = dict()

        variable = tk.StringVar(course_info_frame, name="var_info")
        variable.set("")  # default value
        self.option_variables["var_info"] = variable
        self.option_menus["var_info"] = tk.OptionMenu(
            course_info_frame, variable, *OPTIONS
        )
        self.option_menus["var_info"].config(width=6)
        self.option_menus["var_info"].pack(side=tk.LEFT, padx=5)
        self.option_variables["var_info"].trace("w", self.info_option_selected)
        self.get_info_button = ttk.Button(
            course_info_frame,
            text="Course Information",
            command=self.show_course_info,
            state=tk.DISABLED,
        )
        self.get_info_button.pack(side=tk.LEFT, padx=5)

        # add a separator between frames
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=8, sticky="ew"
        )

        l1 = tk.Label(main_frame, text="AP/Transfer")
        l1.grid(row=2, column=0, sticky=tk.W, pady=2)
        for row in range(5):
            name = "var_0_" + str(row)

            variable = tk.StringVar(main_frame, name=name)
            variable.set("")  # default value
            self.option_variables[name] = variable

            self.option_menus[name] = tk.OptionMenu(main_frame, variable, *OPTIONS)
            w = self.option_menus[name]
            w.config(width=6)
            w.grid(row=row + 3, column=0, sticky=tk.W, pady=2)
            # create a callback for when the user changes the dropdown
            variable.trace("w", self.course_option_selected)

        for sem in range(8):
            l1 = tk.Label(main_frame, text="S" + str(sem + 1))
            l1.grid(row=2, column=sem + 1, sticky=tk.W, pady=2)
            for i in range(5):
                name = "var_" + str(sem + 1) + "_" + str(i)

                variable = tk.StringVar(main_frame, name=name)
                variable.set("")  # default value
                self.option_variables[name] = variable

                self.option_menus[name] = tk.OptionMenu(main_frame, variable, *OPTIONS)
                w = self.option_menus[name]
                w.config(width=6)
                w.grid(row=i + 3, column=sem + 1, sticky=tk.W, pady=2)
                # create a callback for when the user changes the dropdown
                variable.trace("w", self.course_option_selected)

        # Add a separate frame for the labels and fields
        total_credits_frame = ttk.Frame(main_frame)
        total_credits_frame.grid(
            row=8, column=0, columnspan=8, padx=10, pady=5, sticky=tk.W
        )

        self.check_schedule_button = ttk.Button(
            total_credits_frame, text="Check Schedule", command=self.check_schedule
        )
        self.check_schedule_button.pack(side=tk.LEFT, padx=5)

        # Add Total Credits label and associated variable to the new frame
        self.total_credits_var = tk.StringVar(value="0")  # Set default value to "0"
        total_credits_label = ttk.Label(total_credits_frame, text="     Total Credits:")
        total_credits_label.pack(side=tk.LEFT)

        total_credits_field = ttk.Entry(
            total_credits_frame, textvariable=self.total_credits_var, state="readonly"
        )
        total_credits_field.pack(side=tk.LEFT)

        self.prereq_var = tk.IntVar()
        prereq_checkbox = tk.Checkbutton(
            total_credits_frame,
            text="Enforce Prerequisites",
            variable=self.prereq_var,
            command=self.prereq_selected,
        )
        prereq_checkbox.pack(side=tk.LEFT, padx=5)

        self.set_state_pulldowns(tk.DISABLED)

    def get_current_schedule(self):
        courses = []
        for sem in range(9):
            courses.append(set())
            for i in range(5):
                name = "var_" + str(sem) + "_" + str(i)
                val = self.option_variables[name].get()
                if val != "":
                    courses[sem].add(val)
        return courses

    def update_credit_total(self):
        credit_tuple = catalog_utils.total_credits(
            self.get_current_schedule(), self.catalog
        )
        if credit_tuple[0] == credit_tuple[1]:
            self.total_credits_var.set(f"{credit_tuple[0]}")
        else:
            self.total_credits_var.set(f"{credit_tuple[0]}-{credit_tuple[1]}")

    def set_current_schedule(self, schedule):
        #  First clear all entries...
        for sem in range(9):
            for i in range(5):
                name = "var_" + str(sem) + "_" + str(i)
                val = self.option_variables[name].set("")

        #  First clear all entries...
        for sem in range(9):
            for i, course in enumerate(schedule[sem]):
                name = "var_" + str(sem) + "_" + str(i)
                val = self.option_variables[name].set(course)

        self.update_credit_total()

    def show_course_info(self):
        course_id = self.option_variables["var_info"].get()
        info = catalog_utils.format_course_info(course_id, self.catalog)
        info_window = tk.Toplevel(self)
        info_window.title(course_id)
        info_window.geometry("400x300")
        info_window.resizable(True, True)

        text = tk.Text(info_window, wrap=tk.WORD, height=10, width=40)
        text.insert(tk.END, info)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(info_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text.yview)

    def update_options(self, name, options):
        menu = self.option_menus[name]["menu"]
        menu.delete(0, "end")
        menu.add_command(
            label="", command=lambda value="": self.option_variables[name].set(value)
        )
        for option in sorted(list(options)):
            menu.add_command(
                label=option,
                command=lambda value=option: self.option_variables[name].set(value),
            )

    def update_available(self):
        schedule = self.get_current_schedule()
        for sem in range(9):
            for i in range(5):
                name = "var_" + str(sem) + "_" + str(i)
                self.update_options(
                    name, catalog_utils.available_classes(schedule, sem, self.catalog)
                )

    def set_state_pulldowns(self, state):
        for sem in range(9):
            for i in range(5):
                name = "var_" + str(sem) + "_" + str(i)
                self.option_menus[name].config(state=state)
        self.option_menus["var_info"].config(state=state)

    def info_option_selected(self, *args):
        course = self.option_variables["var_info"].get()
        if course == "":
            self.get_info_button.config(state=tk.DISABLED)
        else:
            self.get_info_button.config(state=tk.NORMAL)

    def course_option_selected(self, *args):
        if self.prereq_var.get() == 1:
            self.update_available()
        self.update_credit_total()

    def open_catalog(self):
        """Open the catalog JSON file and parse it into a tree"""
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select Catalog JSON",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
        )
        if filename:
            self.catalog = catalog_utils.load_catalog(filename)
            ids = self.catalog.keys()

            self.update_options("var_info", ids)
            for sem in range(9):
                for i in range(5):
                    name = "var_" + str(sem) + "_" + str(i)
                    self.update_options(name, ids)
            self.set_state_pulldowns(tk.NORMAL)
            self.filemenu.entryconfig("Load Schedule JSON...", state=tk.NORMAL)
            self.filemenu.entryconfig("Save Schedule JSON...", state=tk.NORMAL)

    def load_schedule(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select Schedule JSON",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
        )
        self.set_current_schedule(schedule_utils.load_schedule(filename))

    def save_schedule(self):
        filename = filedialog.asksaveasfilename(
            initialdir=".",
            title="Select Save Location",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
        )
        schedule_utils.save_schedule(self.get_current_schedule(), filename)

    def check_schedule(self):
        sched = self.get_current_schedule()
        dups = schedule_utils.get_duplicates(sched)
        unmet = catalog_utils.check_prerequisites(sched, self.catalog)

        feedback = ""
        if len(dups) == 0 and len(unmet) == 0:
            feedback = "Looks good!"
        else:
            if len(dups) > 0:
                feedback += "Duplicate courses: " + ", ".join(list(sorted(dups))) + "\n\n"
            if len(unmet) > 0:
                feedback += "Courses with unmet prereqs: " + ", ".join(list(sorted(unmet))) + "\n"

        info_window = tk.Toplevel(self)
        info_window.title("Schedule Evaluation")
        info_window.geometry("400x300")
        info_window.resizable(True, True)

        text = tk.Text(info_window, wrap=tk.WORD, height=10, width=40)
        text.insert(tk.END, feedback)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(info_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text.yview)

    def prereq_selected(self):
        if self.prereq_var.get() == 1:
            self.update_available()
        else:
            ids = self.catalog.keys()
            for sem in range(9):
                for i in range(5):
                    name = "var_" + str(sem) + "_" + str(i)
                    self.update_options(name, ids)


if __name__ == "__main__":
    app = App()
    app.mainloop()
