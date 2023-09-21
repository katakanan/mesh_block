import asyncio
from meshlib import MESH, MESH_TYPE, MESH_MSG
import tkinter as tk

bu_block = MESH(MESH_TYPE.MESH_100BU)
# ac_block = MESH(MESH_TYPE.MESH_100AC)

class App:
    def __init__(self, root):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.root = root
        root.title("Tkinter with asyncio")
        label = tk.Label(root, text="Hello, Tkinter!")
        label.pack()
        button = tk.Button(root, text="Find Block", command=lambda:loop.run_in_executor(None, tasks))
        button.pack()
        test_btn = tk.Button(root, text="hello", command=lambda:loop.run_in_executor(None, say_hello))
        test_btn.pack()

def say_hello():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(exit_ble([bu_block]))
    print("Exit")

async def exit_ble(block_list):
    tasks = [block.push_msg(MESH_MSG.EXIT) for block in block_list]
    await asyncio.gather(*tasks)

def tasks():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(mesh_tasks([bu_block]))

async def mesh_tasks(block_list):
    tasks = [asyncio.create_task(block.main()) for block in block_list]

    await asyncio.gather(*tasks)

def main():
    root = tk.Tk()
    root.geometry("300x200")
    app = App(root)
    root.mainloop()

# Initialize event loop
if __name__ == "__main__":
    main()

