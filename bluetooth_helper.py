# bluetooth_helper.py

def list_bluetooth_devices():
    try:
        from jnius import autoclass
        BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
        adapter = BluetoothAdapter.getDefaultAdapter()
        if adapter is None or not adapter.isEnabled():
            return []
        result = []
        bonded = adapter.getBondedDevices()
        for device in bonded.toArray():
            result.append({
                "name": device.getName(),
                "address": device.getAddress(),
            })
        return result
    except Exception as e:
        print(f"BT error: {e}")
        return []


def list_audio_devices():
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        AudioManager = autoclass("android.media.AudioManager")
        activity = PythonActivity.mActivity
        am = activity.getSystemService("audio")

        TYPE_BUILTIN_MIC = 15
        TYPE_BLUETOOTH_SCO = 7
        TYPE_BLUETOOTH_A2DP = 8
        TYPE_WIRED_HEADSET = 3
        TYPE_WIRED_HEADPHONES = 4
        TYPE_USB_DEVICE = 11
        TYPE_BUILTIN_SPEAKER = 2
        TYPE_BLE_HEADSET = 26

        mics = []
        outputs = []

        devices = am.getDevices(AudioManager.GET_DEVICES_ALL).toArray()
        for d in devices:
            t = d.getType()
            name = d.getProductName().toString() if d.getProductName() else f"Type {t}"
            item = {"id": d.getId(), "name": name, "type": t}
            if t in (TYPE_BUILTIN_MIC, TYPE_BLUETOOTH_SCO, TYPE_BLE_HEADSET,
                     TYPE_WIRED_HEADSET, TYPE_USB_DEVICE):
                mics.append(item)
            if t in (TYPE_BUILTIN_SPEAKER, TYPE_BLUETOOTH_A2DP, TYPE_BLUETOOTH_SCO,
                     TYPE_BLE_HEADSET, TYPE_WIRED_HEADPHONES, TYPE_WIRED_HEADSET,
                     TYPE_USB_DEVICE):
                outputs.append(item)

        return {"mics": mics, "outputs": outputs}
    except Exception as e:
        print(f"Audio list error: {e}")
        return {"mics": [], "outputs": []}
