from enum import Enum


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


class MESH_TYPE(Enum):
    MESH_100BU = "MESH-100BU"
    MESH_100LE = "MESH-100LE"
    MESH_100GP = "MESH-100GP"


class MESH:
    def __init__(self, name: MESH_TYPE, event: MESH_EVENT = None):
        self.name = name
        default_event = MESH_EVENT()
        self.event = default_event if event == None else event

    def scan(self):
        while True:
            print("scan...")
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

            await asyncio.sleep(10)


class MESH_EVENT:
    def on_receive_indicate(sender, data: bytearray):
        data = bytes(data)
        print("[indicate]", data)

    def on_receive_notify(sender, data: bytearray):
        if (
            data[MESSAGE_TYPE_INDEX] != MESSAGE_TYPE_ID
            and data[EVENT_TYPE_INDEX] != EVENT_TYPE_ID
        ):
            return

        # use data[..]

        return
