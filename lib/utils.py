import tkinter as tk
from tkinter import ttk
from os import system
import subprocess


class NetConns:
    def __init__(self, frame):
        self.win = frame
        self.listbox = None
        self.treeview = None
        self.scrollbar = None
        self.label = None
        self.labels = None
        self.last_sorted_by = None
        self.last_sort_order = None
        self.make_label()
        self.make_treeview()

    def make_label(self):
        # Make the label
        self.label = tk.Label(self.win, text="Current Network Connections",
                              padx=10, pady=10)
        self.label.grid(row=0, column=0)

    def make_treeview(self):
        data = self.get_network_connections()
        self.labels = ["Proto", "Recv-Q", "Send-Q", "Local Address",
                       "Foreign Address", "State", "PID/Program name"]

        # Make the treeview
        self.treeview = ttk.Treeview(self.win, columns=self.labels,
                                     show="headings", height=20)
        for i in range(len(self.labels)):
            self.treeview.column(i, minwidth=0, width=len(self.labels[i]) * 11,
                                 stretch=tk.NO)
            self.treeview.heading(i, text=self.labels[i])

        self.treeview.grid(row=1, column=0)
        self.scrollbar = tk.Scrollbar(self.win)
        self.scrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.treeview.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.treeview.yview)
        self.treeview.bind("<Double-1>", self.on_double_click)

        # Make the columns sortable
        for i in self.labels:
            self.treeview_sort_column(self.treeview, i, False)

        self.insert_data(data)

    def on_double_click(self, event):
        try:
            item = self.treeview.selection()[0]
            details = self.treeview.item(item, "values")
            ItemDetails(self.win, details)
        except IndexError:
            pass

    def insert_data(self, data):
        # Validate data then insert into treeview
        l_data = data
        l_data.pop()
        for line in l_data[1:]:
            lline = line.split()
            last = lline[-1:]
            for i in last:
                val = i
            if len(val) == 1 and len(lline) != 0 and val != "-":
                x = lline.pop()
                lline[-1] = lline[-1] + x
            if len(lline) < 7:
                lline.insert(5, "N/A")
            if len(lline) == 0:
                continue
            self.treeview.insert("", "end", values=lline)

    def treeview_sort_column(self, treeview: ttk.Treeview, col, reverse: bool):
        """
        to sort the table by column when clicking in column
        """
        def set_sorted_by(col):
            self.last_sorted_by = col
            self.last_sort_order = not reverse
        try:
            data_list = [
                (int(treeview.set(k, col)), k) for k in treeview.get_children("")
            ]
        except Exception:
            data_list = [(treeview.set(k, col), k) for k in treeview.get_children("")]

        data_list.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(data_list):
            treeview.move(k, "", index)

        # reverse sort next time
        treeview.heading(
            column=col,
            text=col,
            command=lambda _col=col: [self.treeview_sort_column(
                treeview, _col, not reverse
            ), set_sorted_by(col)],
        )

    @staticmethod
    def get_network_connections():
        # Get the network connections

        output = subprocess.check_output("netstat -tunap", shell=True)
        output = output.decode("utf-8")
        output = output.split("\n")
        del output[0]
        return output

    def refresh_connections(self):
        # Refresh the network connections
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        self.insert_data(self.get_network_connections())
        if self.last_sorted_by is not None:
            self.treeview_sort_column(self.treeview, self.last_sorted_by,
                                      self.last_sort_order)


class ItemDetails:
    def __init__(self, frame, item):
        self.app = frame.winfo_toplevel()
        self.win = tk.Toplevel(self.app)
        self.win.attributes("-topmost", True)
        self.src = item[3].split(":")
        self.dst = item[4].split(":")
        self.proc = item[6].split("/")[0]
        self.title = (f"Item Details [{self.proc}] {self.src[0]}:{self.src[1]} "
                      f"-> {self.dst[0]}:{self.dst[1]}")
        self.win.title(self.title)
        self.title_label = None
        self.button_frame = None
        self.proc_button = None
        self.traffic_button = None
        self.term_frame = None
        self.proc_frame = None
        self.term = None
        self.make_buttons()

    def make_buttons(self):
        self.title_label = tk.Label(self.win, text=self.title, padx=10,
                                    pady=10, relief=tk.RAISED)
        self.title_label.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.button_frame = tk.Frame(self.win, padx=10, pady=10)
        self.button_frame.grid(row=1, column=0)
        self.traffic_button = tk.Button(self.button_frame, text="Dump Traffic",
                                command=self.dump_traffic, padx=10, pady=10)
        self.traffic_button.grid(row=0, column=0)
        self.proc_button = tk.Button(self.button_frame, text="Process Info",
                                command=self.process_info, padx=10, pady=10)
        self.proc_button.grid(row=0, column=1)
        if self.proc == "-":
            self.proc_button.config(state=tk.DISABLED)

    def dump_traffic(self):
        if self.proc_frame:
            self.proc_frame.destroy()
        self.term_frame = tk.Frame(self.win, padx=10, pady=10)
        self.term_frame.grid(row=2, column=0)
        term_f = tk.Frame(self.term_frame, padx=10, pady=10, height=500,
                          width=700)
        term_f.pack(fill=tk.BOTH, expand=True)
        wid = term_f.winfo_id()

        cmd = f"tcpdump -i any -XXvvv src {self.src[0]} and dst " + \
                    f"{self.dst[0]} and src port {self.src[1]} and dst port" + \
                    f" {self.dst[1]}"
        self.term = system(f"xterm -into {wid} -fn 'DejaVu Sans "
                           f"Mono:size=12' -geometry 150x100 -e '{cmd}' &")

    def process_info(self):
        if self.term_frame:
            self.term_frame.destroy()
        self.proc_frame = tk.Frame(self.win, padx=10, pady=10)
        self.proc_frame.grid(row=2, column=0)
        proc_info = self.get_process_info()

        self.main_p_frame = tk.Frame(self.proc_frame, padx=10, pady=10)
        self.main_p_frame.grid(row=0, column=0)
        self.fill_main_p(proc_info["proc_d"])

        self.args_list = tk.Listbox(self.proc_frame, height=10, width=50)
        self.args_list.grid(row=1, column=0)
        # add vertical and horizontal scrollbars
        ags_y_scrollbar = tk.Scrollbar(self.proc_frame, orient=tk.VERTICAL)
        ags_y_scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
        ags_x_scrollbar = tk.Scrollbar(self.proc_frame, orient=tk.HORIZONTAL)
        ags_x_scrollbar.grid(row=2, column=0, sticky=tk.W+tk.E)
        # configure the listbox to use the scrollbars
        self.args_list.configure(yscrollcommand=ags_y_scrollbar.set)
        self.args_list.configure(xscrollcommand=ags_x_scrollbar.set)
        # configure the scrollbars to use the listbox
        ags_y_scrollbar.configure(command=self.args_list.yview)
        ags_x_scrollbar.configure(command=self.args_list.xview)

        self.treeview = tk.Frame(self.proc_frame, padx=10, pady=10,
                                 height=50,
                                 width=self.args_list.winfo_width())
        p_tree_title = tk.Label(self.proc_frame, text="Process Tree",
                                padx=10, pady=10)
        p_tree_title.grid(row=3, column=0)
        tree_label = tk.Text(self.treeview)
        tree_label.insert(tk.END, proc_info["tree"])
        self.treeview.grid(row=4, column=0)
        tree_label.grid(row=0, column=0)
        tv_y_scrollbar = tk.Scrollbar(self.treeview, orient=tk.VERTICAL)
        tv_y_scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        tv_x_scrollbar = tk.Scrollbar(self.treeview, orient=tk.HORIZONTAL)
        tv_x_scrollbar.grid(row=1, column=0, sticky=tk.W+tk.E)
        tv_x_scrollbar.configure(command=tree_label.xview)
        tv_y_scrollbar.configure(command=tree_label.yview)

        self.fill_args(proc_info["args"])



    def fill_main_p(self, data):
        labels = data.split("\n")[0].split()
        main_p_dict = {}
        for label in labels:
            main_p_dict[label] = tk.Label(self.main_p_frame, text=label, font="bold")
            main_p_dict[label].grid(row=0, column=labels.index(label))
        data = data.split("\n")[1]
        data = data.split()
        for idx, item in enumerate(data):
            main_p_dict[f"{idx}{item}"] = tk.Label(self.main_p_frame,
                                                   text=item)
            main_p_dict[f"{idx}{item}"].grid(row=1, column=idx, pady=3)

    def fill_args(self, data):
        args = data.split()
        for arg in args:
            self.args_list.insert(tk.END, arg)

    def get_process_info(self):
        p_dict = {"proc_d": subprocess.check_output(f"ps -p {self.proc} -o pid,ppid,"
                                        f"vsz=MEMORY "
                                   f"-o "
                                   f"user,"
                                   f"group=GROUP -o comm", shell=True).decode("utf-8"),
                  "args": subprocess.check_output(f"ps -p {self.proc} -o "
                                                  f"args=ARGS", shell=True).decode("utf-8"),
                  "tree": subprocess.check_output(f"pstree -p {self.proc}",
                                                  shell=True).decode("utf-8")}
        return p_dict
