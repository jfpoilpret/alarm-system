from app.models import Device

class DeviceKind:
    def __init__(self, allowed_ids, threshold = 2.7):
        self.allowed_ids = allowed_ids
        self.threshold = threshold

device_kinds = {
    Device.KIND_KEYPAD: DeviceKind([0x10, 0x11, 0x12, 0x13]),
    Device.KIND_MOTION: DeviceKind([0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]),
    Device.KIND_CAMERA: DeviceKind([0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37]),
}
