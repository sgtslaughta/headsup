import tkinter as tk
from tkinter import ttk


class NetConns:
    def __init__(self, frame):
        self.win = frame
        self.listbox = None
        self.treeview = None
        self.scrollbar = None
        self.label = None
        self.labels = None
        self.last_sorted_by = None
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

        # Make the columns sortable
        for i in self.labels:
            self.treeview_sort_column(self.treeview, i, False)

        self.insert_data(data)

    def insert_data(self, data):
        # Validate data then insert into treeview
        l_data = data
        l_data.pop()
        for line in l_data[1:]:
            lline = line.split()
            last = lline[-1:]
            for i in last:
                val = i
            if len(val) == 1 and len(lline) != 0:
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
        print(self.last_sorted_by)

    @staticmethod
    def get_network_connections():
        # Get the network connections
        import subprocess
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
        self.treeview_sort_column(self.treeview, self.last_sorted_by, False)
