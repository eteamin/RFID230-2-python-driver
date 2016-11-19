import unittest
import threading
import time

from rfid.main import Driver


ENCRYPTION_KEY = 281474976710655
expected_resp = b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
                b'0000000ff078069ffffffffffff'


class TestCase(unittest.TestCase):
    def setUp(self):
        self.serial_path = '/dev/ttyUSB0'
        self.timeout = 1
        self.driver = Driver(self.serial_path, timeout=self.timeout, encrypion_key=ENCRYPTION_KEY)

        # Summoning a worker thread to read the card
        self.resp_from_card = None
        self.worker = threading.Thread(target=self.worker, daemon=True)
        self.start_time = time.time()
        self.worker.start()

    def worker(self):
        self.resp_from_card = self.driver.loop()

    def test_read(self):
        deadline = time.time() + 2 * 1
        while time.time() < deadline:
            time.sleep(0.01)
            continue
        self.assertEqual(self.resp_from_card, expected_resp)


if __name__ == '__main__':
    unittest.main()
