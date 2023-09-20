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
        button = tk.Button(root, text="Start Asyncio", command=lambda:loop.run_in_executor(None, tasks))
        button.pack()

def tasks():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(mesh_tasks())

async def mesh_tasks():
    bu_block = MESH(MESH_TYPE.MESH_100BU)
    task = asyncio.create_task(bu_block.main())
    ac_block = MESH(MESH_TYPE.MESH_100AC)
    task2 = asyncio.create_task(ac_block.main())

    await asyncio.gather(task, task2)

def main():
    root = tk.Tk()
    root.geometry("300x200")
    app = App(root)
    root.mainloop()

# Initialize event loop
if __name__ == "__main__":
    main()

