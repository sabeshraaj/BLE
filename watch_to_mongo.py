import asyncio
from bleak import BleakClient
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
# change the mongo_uri according to your own mongo local server connect
# if you are trying to access the mongodb from a different machine change it according to your own ip address
mongo_uri = " " 
client_mongo = MongoClient(mongo_uri)
db = client_mongo["your_own_database"]
collection = db["your_own_collection"]

# BLE Configuration
address = "XX:XX:XX:XX:XX:XX"  #replace this with BLE MAC address of the watch you are trying to connect and collect data from 
write_uuid = "f0001200-0551-4000-b000-000000000000"    # check with the characteristics of your own watch and change accordingly 
notify_uuid = "f0001100-0551-4000-b000-000000000000"   # check with the charactersitics of your own watch and change accordingly

ble_client = None  # Will be assigned in run()

# Temperature combining function
def temp_comb(temp_dec, temp_point):
    return round(temp_dec + 0.01 * temp_point, 2)

# MongoDB document inserter
def store_to_mongo(data_dict):
    document = {
        "patient_id": "p1",
        "watch_id": address,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "pulse_pressure": data_dict["pulse_pressure"],
        "temperature": data_dict["temperature"],
        "spo2": data_dict["spo2"],
        "respiratory_rate": data_dict["respiratory_rate"]
    }
    collection.insert_one(document)
    print("🗂️ Data inserted into MongoDB:", document)

# Notification handler
def notification_handler(sender, data):
    print(f"\n🔔 Data from {sender}: {data.hex().upper()}")

    try:
        hex_bytes = list(data)

        pulse_pressure = int(hex_bytes[0])           # 0x44 = 68
        temp_point = int(hex_bytes[1])               # 0x0A = 10
        temp_dec = int(hex_bytes[2])                 # 0xF0 = 240
        # hex_bytes[3] is unused
        spo2 = int(hex_bytes[4])                     # 0x52 = 82
        respiratory_rate = int(hex_bytes[5])         # 0x0F = 15
        # hex_bytes[6] is request code (ignore)

        temperature = temp_comb(temp_dec, temp_point)

        parsed_data = {
            "pulse_pressure": pulse_pressure,
            "temperature": temperature,
            "spo2": spo2,
            "respiratory_rate": respiratory_rate
        }

        store_to_mongo(parsed_data)

    except Exception as e:
        print("❌ Error parsing BLE data:", e)

    asyncio.create_task(send_command())

# Send command to start reading
async def send_command():
    print("📤 Sending command 'E1' to start measurement...")
    await ble_client.write_gatt_char(write_uuid, bytearray.fromhex("E1"))
    print("✅ Command sent.")

# BLE runner
async def run():
    global ble_client
    async with BleakClient(address) as ble_client:
        if ble_client.is_connected:
            print("✅ Connected to Vincense Watch!")
            await ble_client.start_notify(notify_uuid, notification_handler)
            print("📡 Subscribed to notifications.")
            await send_command()

            while True:
                await asyncio.sleep(1)
        else:
            print("❌ Could not connect to device.")

if __name__ == "__main__":
    asyncio.run(run())
