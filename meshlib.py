from enum import Enum
import asyncio
from bleak import BleakClient, discover
from struct import pack

# UUID
CORE_INDICATE_UUID = "72c90005-57a9-4d40-b746-534e22ec9f9e"
CORE_NOTIFY_UUID = "72c90003-57a9-4d40-b746-534e22ec9f9e"
CORE_WRITE_UUID = "72c90004-57a9-4d40-b746-534e22ec9f9e"

# Constant values
MESSAGE_TYPE_INDEX = 0
EVENT_TYPE_INDEX = 1
STATE_INDEX = 2
MESSAGE_TYPE_ID = 1
EVENT_TYPE_ID = 0

class MESH_MSG(Enum):
    EXIT = 0

class MESH_TYPE(Enum):
    MESH_100BU = "MESH-100BU"
    MESH_100LE = "MESH-100LE"
    MESH_100GP = "MESH-100GP"
    MESH_100AC = "MESH-100AC"

class MESH_EVENT:
    def __init__(self) -> None:
        self.name = ""
        self.event_counter = 0

    def on_receive_indicate(self, sender, data: bytearray):
        data = bytes(data)
        print("[indicate]", data)

    def on_receive_notify(self, sender, data: bytearray):
        if (
            data[MESSAGE_TYPE_INDEX] != MESSAGE_TYPE_ID
            and data[EVENT_TYPE_INDEX] != EVENT_TYPE_ID
        ):
            return

        # use data[..]
        print(self.name, "'s Event Received", self.event_counter)
        self.event_counter = self.event_counter + 1

        return

class MESH:
    def __init__(self, mesh_type: MESH_TYPE, event: MESH_EVENT = None):
        self.name = mesh_type.value
        self.event = MESH_EVENT() if event == None else event
        self.event.name = self.name
        self.queue = asyncio.Queue()

    async def push_msg(self, msg:MESH_MSG):
        await self.queue.put(msg)

    async def scan(self):
        while True:
            print("scan ", self.name ,"...")
            try:
                return next(
                    d
                    for d in await discover()
                    if d.name and d.name.startswith(self.name)
                )
            except StopIteration:
                continue

    async def main(self):
        device = await self.scan()
        print("found", device.name, device.address)

        async with BleakClient(device, timeout=None) as client:
            await client.start_notify(CORE_NOTIFY_UUID, self.event.on_receive_notify)
            await client.start_notify(
                CORE_INDICATE_UUID, self.event.on_receive_indicate
            )
            await client.write_gatt_char(
                CORE_WRITE_UUID, pack("<BBBB", 0, 2, 1, 3), response=True
            )
            print(device.name, "is connected.")
            self.queue = asyncio.Queue()
            
            while True:
                await asyncio.sleep(0.5)
                if not self.queue.empty() and await self.queue.get() == MESH_MSG.EXIT:
                    print(device.name, "Exit msg received")
                    await client.disconnect() #?
                    self.event.event_counter = self.event.event_counter - 1
                    break

            print(device.name, "is Ended.")

