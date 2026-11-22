import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def get_height(self):
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._get_height_recursive(node.left), self._get_height_recursive(node.right))

    def count_nodes(self):
        return self._count_nodes_recursive(self.root)

    def _count_nodes_recursive(self, node):
        if node is None:
            return 0
        return 1 + self._count_nodes_recursive(node.left) + self._count_nodes_recursive(node.right)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def preorder(self, node, result=None):
        if result is None: result = []
        if node:
            result.append(node.value)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result

    def inorder(self, node, result=None):
        if result is None: result = []
        if node:
            self.inorder(node.left, result)
            result.append(node.value)
            self.inorder(node.right, result)
        return result

    def postorder(self, node, result=None):
        if result is None: result = []
        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.value)
        return result

class BSTApp:
    def __init__(self, root_window):
        self.window = root_window
        self.window.title("Fase4NathaliaRangel - BST Explorer")
        self.window.geometry("1200x700")
        self.window.configure(bg="#1e1e2e")
        
        self.tree = BST()
        self.node_radius = 20
        self.x_spacing = 50
        self.y_spacing = 80
        self.node_positions = {}

        self.left_panel = tk.Frame(self.window, bg="#282a36", width=250)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(self.left_panel, text="Controls", fg="white", bg="#282a36", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self.left_panel, text="Node Value (Integer):", fg="white", bg="#282a36").pack(anchor="w")
        self.entry_value = tk.Entry(self.left_panel)
        self.entry_value.pack(fill=tk.X, pady=5)

        tk.Button(self.left_panel, text="➕ Add Node", bg="#4CAF50", fg="white", command=self.add_node).pack(fill=tk.X, pady=5)
        tk.Button(self.left_panel, text="🔍 Search Node", bg="#2196F3", fg="white", command=self.search_node).pack(fill=tk.X, pady=5)
        tk.Button(self.left_panel, text="🧹 Clear Tree", bg="#FF9800", fg="white", command=self.clear_tree).pack(fill=tk.X, pady=5)
        tk.Button(self.left_panel, text="🚪 Exit", bg="#f44336", fg="white", command=self.window.destroy).pack(fill=tk.X, pady=5)

        self.stats_label = tk.Label(self.left_panel, text="Nodes: 0\nHeight: 0", fg="#a6e3a1", bg="#282a36", justify=tk.LEFT)
        self.stats_label.pack(anchor="w", pady=20)

        self.right_panel = tk.Frame(self.window, bg="#1e1e2e")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_tree = tk.Canvas(self.right_panel, bg="#11111b", highlightthickness=0)
        self.canvas_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.traversal_frame = tk.Frame(self.right_panel, bg="#1e1e2e", height=100)
        self.traversal_frame.pack(fill=tk.X, padx=10, pady=10)

        self.lbl_preorder = self.create_traversal_panel("Pre-order", 0)
        self.lbl_inorder = self.create_traversal_panel("In-order", 1)
        self.lbl_postorder = self.create_traversal_panel("Post-order", 2)

    def create_traversal_panel(self, title, col):
        frame = tk.Frame(self.traversal_frame, bg="#282a36", bd=2, relief=tk.RIDGE)
        frame.grid(row=0, column=col, padx=5, sticky="nsew")
        self.traversal_frame.grid_columnconfigure(col, weight=1)
        tk.Label(frame, text=title, fg="#89b4fa", bg="#282a36", font=("Arial", 10, "bold")).pack(anchor="w")
        lbl = tk.Label(frame, text="-", fg="white", bg="#282a36", wraplength=250, justify=tk.LEFT)
        lbl.pack(anchor="w")
        return lbl

    def add_node(self):
        try:
            val = int(self.entry_value.get())
            if self.tree.search(val):
                messagebox.showwarning("Duplicate", f"Node {val} already exists in the tree.")
                return
      
            self.tree.insert(val)
            if self.tree.get_height() > 4:
                self.tree.root = self._remove_node(self.tree.root, val) # Revertir
                messagebox.showerror("Max Level Reached", "Adding this node would create level 5.\nThe tree is limited to 4 levels.")
                return

            self.entry_value.delete(0, tk.END)
            self.draw_tree()
            self.update_stats()
            self.update_traversals()
        except ValueError:
            messagebox.showerror("Invalid Input", f"'{self.entry_value.get()}' is not a valid integer.\nOnly whole numbers are accepted.")
            self.entry_value.delete(0, tk.END)

    def search_node(self):
        try:
            val = int(self.entry_value.get())
            if self.tree.search(val):
                messagebox.showinfo("Node Found", f"Node {val} was found in the tree.")
            else:
                messagebox.showinfo("Node Not Found", f"Node {val} was NOT found in the tree.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer to search.")

    def clear_tree(self):
        self.tree = BST()
        self.canvas_tree.delete("all")
        self.update_stats()
        self.update_traversals()
        self.entry_value.delete(0, tk.END)

    def update_stats(self):
        nodes = self.tree.count_nodes()
        height = self.tree.get_height()
        self.stats_label.config(text=f"Nodes: {nodes}\nHeight: {height}")

    def update_traversals(self):
        pre = ", ".join(map(str, self.tree.preorder(self.tree.root))) or "-"
        ino = ", ".join(map(str, self.tree.inorder(self.tree.root))) or "-"
        post = ", ".join(map(str, self.tree.postorder(self.tree.root))) or "-"
        
        self.lbl_preorder.config(text=pre)
        self.lbl_inorder.config(text=ino)
        self.lbl_postorder.config(text=post)

    def draw_tree(self):
        self.canvas_tree.delete("all")
        self.node_positions.clear()
        if self.tree.root:
            canvas_width = self.canvas_tree.winfo_width() or 800
            self._draw_recursive(self.tree.root, canvas_width // 2, 50, canvas_width // 4)

    def _draw_recursive(self, node, x, y, x_offset):
        if node is None: return
        
        if node.left:
            self.canvas_tree.create_line(x, y, x - x_offset, y + self.y_spacing, fill="#89b4fa", width=2)
            self._draw_recursive(node.left, x - x_offset, y + self.y_spacing, x_offset // 2)
        if node.right:
            self.canvas_tree.create_line(x, y, x + x_offset, y + self.y_spacing, fill="#89b4fa", width=2)
            self._draw_recursive(node.right, x + x_offset, y + self.y_spacing, x_offset // 2)

        self.node_positions[node.value] = (x, y)
        self.canvas_tree.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill="#89b4fa", outline="white", width=2)
        self.canvas_tree.create_text(x, y, text=str(node.value), fill="#11111b", font=("Arial", 12, "bold"))

    def _remove_node(self, node, val):

        if node is None: return node
        if val < node.value: node.left = self._remove_node(node.left, val)
        elif val > node.value: node.right = self._remove_node(node.right, val)
        else:
            if node.left is None: return node.right
            elif node.right is None: return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._remove_node(node.right, temp.value)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

class LoginApp:
    def __init__(self, root_window):
        self.window = root_window
        self.window.title("Fase4NathaliaRangel - Login")
        self.window.geometry("500x400")
        self.window.configure(bg="#1e1e2e")
        
        self.window.eval('tk::PlaceWindow . center')

        tk.Label(self.window, text="🔺 BST Explorer", fg="#00bcd4", bg="#1e1e2e", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.window, text="Binary Search Tree - Phase 4", fg="#a6e3a1", bg="#1e1e2e", font=("Arial", 12)).pack()

        info_frame = tk.Frame(self.window, bg="#282a36", bd=2, relief=tk.RIDGE)
        info_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(info_frame, text="Application: Fase4NathaliaRangel", fg="white", bg="#282a36", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(info_frame, text="Student: Lineth Nathalia Rangel", fg="white", bg="#282a36", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(info_frame, text="Course: Data Structures - 301305A_2204", fg="white", bg="#282a36", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(info_frame, text=f"Date: {datetime.now().strftime('%B %d, %Y')}", fg="white", bg="#282a36", anchor="w").pack(fill=tk.X, padx=10, pady=2)

        tk.Label(self.window, text="Enter Password:", fg="white", bg="#1e1e2e", anchor="w").pack(fill=tk.X, padx=30)
        
        self.entry_pass = tk.Entry(self.window, show="*", bg="#282a36", fg="white", insertbackground="white")
        self.entry_pass.pack(fill=tk.X, padx=30, pady=5)

        tk.Button(self.window, text="Access BST Explorer ➔", bg="#00bcd4", fg="white", font=("Arial", 12, "bold"), command=self.check_password).pack(fill=tk.X, padx=30, pady=20)

    def check_password(self):
        if self.entry_pass.get() == "UNAD":
            self.window.destroy()
            root = tk.Tk()
            app = BSTApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect password. Hint: UNAD")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()