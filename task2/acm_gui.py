import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ACMTool:
    def __init__(self, root):
        self.root = root
        self.root.title("访问控制矩阵演示系统")
        self.root.geometry("800x600")

        # Data Structure: matrix[subject][object] = {set of permissions}
        self.subjects = []
        self.objects = []
        self.matrix = {} # Dict of Dict of Sets

        # Top Control Panel
        control_frame = tk.Frame(root)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(control_frame, text="添加主体(Subject)", command=self.add_subject).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="添加客体(Object)", command=self.add_object).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="修改权限", command=self.edit_permission).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="检查权限", command=self.check_permission_dialog).pack(side=tk.LEFT, padx=5)

        # Matrix View
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("Subject"), show="headings")
        self.tree.heading("Subject", text="主体 \\ 客体")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Initialize some data
        self.init_data()
        self.refresh_view()

    def init_data(self):
        self.add_subject_logic("Alice")
        self.add_subject_logic("Bob")
        self.add_subject_logic("Admin")
        
        self.add_object_logic("File1.txt")
        self.add_object_logic("File2.txt")
        self.add_object_logic("App.exe")

        self.set_permission("Alice", "File1.txt", {"Read", "Write"})
        self.set_permission("Bob", "File1.txt", {"Read"})
        self.set_permission("Admin", "File1.txt", {"Read", "Write", "Own"})
        self.set_permission("Admin", "App.exe", {"Execute"})

    def add_subject_logic(self, name):
        if name and name not in self.subjects:
            self.subjects.append(name)
            self.matrix[name] = {}
            for obj in self.objects:
                self.matrix[name][obj] = set()

    def add_object_logic(self, name):
        if name and name not in self.objects:
            self.objects.append(name)
            for sub in self.subjects:
                if name not in self.matrix[sub]:
                    self.matrix[sub][name] = set()

    def set_permission(self, sub, obj, rights):
        if sub in self.subjects and obj in self.objects:
            self.matrix[sub][obj] = rights

    def add_subject(self):
        name = simpledialog.askstring("输入", "请输入主体名称:")
        if name:
            if name in self.subjects:
                messagebox.showerror("错误", "主体已存在")
            else:
                self.add_subject_logic(name)
                self.refresh_view()

    def add_object(self):
        name = simpledialog.askstring("输入", "请输入客体名称:")
        if name:
            if name in self.objects:
                messagebox.showerror("错误", "客体已存在")
            else:
                self.add_object_logic(name)
                self.refresh_view()

    def edit_permission(self):
        # Create a custom dialog window
        top = tk.Toplevel(self.root)
        top.title("修改权限")

        tk.Label(top, text="主体:").grid(row=0, column=0)
        sub_var = tk.StringVar(value=self.subjects[0] if self.subjects else "")
        sub_cb = ttk.Combobox(top, textvariable=sub_var, values=self.subjects)
        sub_cb.grid(row=0, column=1)

        tk.Label(top, text="客体:").grid(row=1, column=0)
        obj_var = tk.StringVar(value=self.objects[0] if self.objects else "")
        obj_cb = ttk.Combobox(top, textvariable=obj_var, values=self.objects)
        obj_cb.grid(row=1, column=1)

        # Checkboxes for permissions
        tk.Label(top, text="权限:").grid(row=2, column=0)
        
        read_var = tk.BooleanVar()
        write_var = tk.BooleanVar()
        exec_var = tk.BooleanVar()
        own_var = tk.BooleanVar()

        tk.Checkbutton(top, text="Read", variable=read_var).grid(row=2, column=1, sticky="w")
        tk.Checkbutton(top, text="Write", variable=write_var).grid(row=3, column=1, sticky="w")
        tk.Checkbutton(top, text="Execute", variable=exec_var).grid(row=4, column=1, sticky="w")
        tk.Checkbutton(top, text="Own", variable=own_var).grid(row=5, column=1, sticky="w")

        def load_current(*args):
            s = sub_var.get()
            o = obj_var.get()
            if s in self.matrix and o in self.matrix[s]:
                perms = self.matrix[s][o]
                read_var.set("Read" in perms)
                write_var.set("Write" in perms)
                exec_var.set("Execute" in perms)
                own_var.set("Own" in perms)
            else:
                read_var.set(False)
                write_var.set(False)
                exec_var.set(False)
                own_var.set(False)

        sub_cb.bind("<<ComboboxSelected>>", load_current)
        obj_cb.bind("<<ComboboxSelected>>", load_current)
        load_current() # Initial load

        def save():
            s = sub_var.get()
            o = obj_var.get()
            new_perms = set()
            if read_var.get(): new_perms.add("Read")
            if write_var.get(): new_perms.add("Write")
            if exec_var.get(): new_perms.add("Execute")
            if own_var.get(): new_perms.add("Own")
            
            self.set_permission(s, o, new_perms)
            self.refresh_view()
            top.destroy()

        tk.Button(top, text="保存", command=save).grid(row=6, column=0, columnspan=2)

    def check_permission_dialog(self):
        top = tk.Toplevel(self.root)
        top.title("检查权限")
        
        tk.Label(top, text="主体:").pack()
        sub_var = tk.StringVar()
        sub_cb = ttk.Combobox(top, textvariable=sub_var, values=self.subjects)
        sub_cb.pack()
        
        tk.Label(top, text="客体:").pack()
        obj_var = tk.StringVar()
        obj_cb = ttk.Combobox(top, textvariable=obj_var, values=self.objects)
        obj_cb.pack()
        
        tk.Label(top, text="请求操作(例如 Read):").pack()
        op_var = tk.StringVar()
        op_entry = tk.Entry(top, textvariable=op_var)
        op_entry.pack()
        
        def check():
            s = sub_var.get()
            o = obj_var.get()
            op = op_var.get()
            if s in self.matrix and o in self.matrix[s]:
                if op in self.matrix[s][o]:
                    messagebox.showinfo("结果", "允许访问 (Allow)")
                else:
                    messagebox.showwarning("结果", "拒绝访问 (Deny)")
            else:
                messagebox.showerror("错误", "主体或客体不存在")

        tk.Button(top, text="验证", command=check).pack()

    def refresh_view(self):
        # Clear current columns and data
        self.tree["columns"] = ["Subject"] + self.objects
        
        self.tree.heading("Subject", text="Subject \\ Object")
        self.tree.column("Subject", width=100, anchor="center")
        
        for obj in self.objects:
            self.tree.heading(obj, text=obj)
            self.tree.column(obj, width=100, anchor="center")
        
        # Clear items
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Insert data
        for sub in self.subjects:
            values = [sub]
            for obj in self.objects:
                perms = self.matrix[sub].get(obj, set())
                values.append(",".join(sorted(list(perms))) if perms else "-")
            self.tree.insert("", "end", values=values)

if __name__ == "__main__":
    root = tk.Tk()
    app = ACMTool(root)
    root.mainloop()

