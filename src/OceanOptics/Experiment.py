import array
import pathlib
import platform
import sys
import threading
import time

import libusb
import matplotlib.pyplot as plt
import usb.backend.libusb1
import usb.core
import usb.util


def main():
    if usb.backend.libusb1.get_backend() is None:
        if platform.system() == "Windows":
            p_path = "x64" if sys.maxsize > 2**32 else "x86"
            dll_path = (
                pathlib.Path(libusb.__file__).parent
                / rf"_platform\_windows\{p_path}\libusb-1.0.dll"
            )
            usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)

    INT_TIME = 500_000

    dev = usb.core.find(idVendor=0x2457, idProduct=0x101E)
    dev.set_configuration()
    dev.write(0x01, b"\x01")
    dev.write(0x01, b"\x02" + int(INT_TIME).to_bytes(4, "little"))

    try:
        while True:
            t0 = time.monotonic()
            dev.write(0x01, b"\x09")
            # wait for measurement to complete
            time.sleep(INT_TIME / 1_000_000)
            packets = []
            while True:
                try:
                    packets.append(dev.read(0x82, 512, 10).tobytes())
                except usb.core.USBTimeoutError:
                    break
            assert packets[-1][-1] == 0x69
            t1 = time.monotonic()

            pixels = array.array("H", b"".join(packets[:-1]))

            plt.clf()
            # plt.scatter(pixels[20:], marker='hd', color='black')
            plt.plot(pixels[20:])
            plt.show()
            print(f"Got {len(pixels)} pixels in {t1 - t0:.1f}s.")
    except KeyboardInterrupt:
        pass

    # Shutdown
    print("Shutting down.")
    dev.write(0x01, b"\x04\x00\x00")


class OceanOpticsController:
    def __init__(self):
        if usb.backend.libusb1.get_backend() is None:
            if platform.system() == "Windows":
                p_path = "x64" if sys.maxsize > 2**32 else "x86"
                dll_path = (
                    pathlib.Path(libusb.__file__).parent
                    / rf"_platform\_windows\{p_path}\libusb-1.0.dll"
                )
                usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)

        self.INT_TIME = 500_000

        self.dev = usb.core.find(idVendor=0x2457, idProduct=0x101E)
        self.dev.set_configuration()
        self.dev.write(0x01, b"\x01")
        self.dev.write(0x01, b"\x02" + int(self.INT_TIME).to_bytes(4, "little"))

        self.running = False

    def data(self):
        self.dev.write(0x01, b"\x09")
        # wait for measurement to complete
        time.sleep(self.INT_TIME / 1_000_000)
        packets = []
        while True:
            try:
                packets.append(self.dev.read(0x82, 512, 10).tobytes())
            except usb.core.USBTimeoutError:
                break
        assert packets[-1][-1] == 0x69

        values = array.array("H", b"".join(packets[:-1]))

        self.dev.write(0x01, b"\x04\x00\x00")

        return values

    def start_scan(self):
        """Start a new thread to execute a scan."""
        self._scan_thread = threading.Thread(target=self.data, args=())
        self._scan_thread.start()

        self.running = True

    def stop_scan(self):
        # self._scan_thread.stop()
        self.running = False


if __name__ == "__main__":
    main()
