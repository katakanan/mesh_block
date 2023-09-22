import asyncio
from meshlib import MESH, MESH_TYPE, MESH_MSG
import tkinter as tk

# bu_block = MESH(MESH_TYPE.MESH_100BU)
# ac_block = MESH(MESH_TYPE.MESH_100AC)


class App:
    def __init__(self, root):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.bu_block = MESH(MESH_TYPE.MESH_100BU)
        self.block_list = [self.bu_block]

        self.root = root
        root.title("Tkinter with asyncio")
        label = tk.Label(root, text="Hello, Tkinter!")
        label.pack()
        button = tk.Button(
            root,
            text="Find Block",
            command=lambda: loop.run_in_executor(None, self.mesh_tasks),
        )
        button.pack()
        test_btn = tk.Button(
            root,
            text="Exit",
            command=lambda: loop.run_in_executor(None, self.exit_connection),
        )
        test_btn.pack()

        msg_btn = tk.Button(
            root,
            text="send msg",
            command=lambda: loop.run_in_executor(
                None, self.send_msg(self.bu_block, MESH_MSG.HOGE)
            ),
        )
        msg_btn.pack()

    def send_msg(self, block, msg):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.async_send_msg(block, msg))

    async def async_send_msg(self, block, msg):
        await asyncio.gather(block.push_msg(msg))
        print("Send", msg, "to", block.name)

    def exit_connection(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.async_exit_connection())
        print("Exit")

    async def async_exit_connection(self):
        tasks = [block.push_msg(MESH_MSG.EXIT) for block in self.block_list]
        await asyncio.gather(*tasks)

    def mesh_tasks(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.async_mesh_tasks())

    async def async_mesh_tasks(self):
        tasks = [asyncio.create_task(block.main()) for block in self.block_list]
        await asyncio.gather(*tasks)


def main():
    root = tk.Tk()
    root.geometry("300x200")
    app = App(root)
    root.mainloop()


# Initialize event loop
if __name__ == "__main__":
    main()
