import asyncio
from meshlib import MESH, MESH_TYPE
import tkinter as tk

class App:
    def __init__(self, root):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.root = root
        root.title("Tkinter with asyncio")
        label = tk.Label(root, text="Hello, Tkinter!")
        label.pack()
        button = tk.Button(root, text="Start Asyncio", command=lambda:loop.run_in_executor(None, mesh_tasks))
        button.pack()


def mesh_tasks():
    bu_block = MESH(MESH_TYPE.MESH_100BU)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(bu_block.main())
    # await bu_block.main()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# Initialize event loop
if __name__ == "__main__":
    main()

