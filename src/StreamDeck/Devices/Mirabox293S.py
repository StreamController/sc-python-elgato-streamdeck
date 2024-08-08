#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#
#   Mirabox Stream Dock 293S support by rescbr

from .StreamDeck import StreamDeck, ControlType


class Mirabox293S(StreamDeck):
    """
    Represents a physically attached Mirabox Stream Dock 293S device.
    """

    KEY_COUNT = 15
    KEY_COLS = 5
    KEY_ROWS = 3

    KEY_PIXEL_WIDTH = 85 # TODO: check if this is the correct value
    KEY_PIXEL_HEIGHT = 85 # TODO: check if this is the correct value
    KEY_IMAGE_FORMAT = "JPEG"
    KEY_FLIP = (False, False)
    KEY_ROTATION = 90

    DECK_TYPE = "Mirabox Stream Dock 293S"
    DECK_VISUAL = True
    DECK_TOUCH = False # kind of... it could be used for the side display.

    PACKET_LENGHT = 512

    # the side display uses key ids 0x10, 0x11, 0x12 with 80x80 images.
    KEY_NUM_TO_DEVICE_KEY_ID = [0x0d, 0x0a, 0x07, 0x04, 0x01, 0xe, 0xb, 0x08, 0x05, 0x02, 0x0f, 0x0c, 0x09, 0x06, 0x03]
    KEY_DEVICE_KEY_ID_TO_NUM = {value: index for index, value in enumerate(KEY_NUM_TO_DEVICE_KEY_ID)}

    # see note in _read_control_states() method.
    _key_triggered_last_read = False

    # 72 x 72 black JPEG
    BLANK_KEY_IMAGE = [
        0xff, 0xd8, 0xff, 0xe0, 0x00, 0x10, 0x4a, 0x46, 0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
        0x00, 0xff, 0xdb, 0x00, 0x43, 0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09, 0x09, 0x08,
        0x0a, 0x0c, 0x14, 0x0d, 0x0c, 0x0b, 0x0b, 0x0c, 0x19, 0x12, 0x13, 0x0f, 0x14, 0x1d, 0x1a, 0x1f, 0x1e, 0x1d, 0x1a,
        0x1c, 0x1c, 0x20, 0x24, 0x2e, 0x27, 0x20, 0x22, 0x2c, 0x23, 0x1c, 0x1c, 0x28, 0x37, 0x29, 0x2c, 0x30, 0x31, 0x34,
        0x34, 0x34, 0x1f, 0x27, 0x39, 0x3d, 0x38, 0x32, 0x3c, 0x2e, 0x33, 0x34, 0x32, 0xff, 0xdb, 0x00, 0x43, 0x01, 0x09,
        0x09, 0x09, 0x0c, 0x0b, 0x0c, 0x18, 0x0d, 0x0d, 0x18, 0x32, 0x21, 0x1c, 0x21, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32,
        0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32,
        0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32,
        0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0xff, 0xc0, 0x00, 0x11, 0x08, 0x00, 0x48, 0x00, 0x48, 0x03, 0x01, 0x22, 0x00,
        0x02, 0x11, 0x01, 0x03, 0x11, 0x01, 0xff, 0xc4, 0x00, 0x1f, 0x00, 0x00, 0x01, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01,
        0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a,
        0x0b, 0xff, 0xc4, 0x00, 0xb5, 0x10, 0x00, 0x02, 0x01, 0x03, 0x03, 0x02, 0x04, 0x03, 0x05, 0x05, 0x04, 0x04, 0x00,
        0x00, 0x01, 0x7d, 0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07,
        0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xa1, 0x08, 0x23, 0x42, 0xb1, 0xc1, 0x15, 0x52, 0xd1, 0xf0, 0x24, 0x33, 0x62,
        0x72, 0x82, 0x09, 0x0a, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x34, 0x35, 0x36, 0x37,
        0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a,
        0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x83, 0x84, 0x85,
        0x86, 0x87, 0x88, 0x89, 0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6,
        0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7,
        0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7,
        0xe8, 0xe9, 0xea, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa, 0xff, 0xc4, 0x00, 0x1f, 0x01, 0x00,
        0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03,
        0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0xff, 0xc4, 0x00, 0xb5, 0x11, 0x00, 0x02, 0x01, 0x02, 0x04, 0x04,
        0x03, 0x04, 0x07, 0x05, 0x04, 0x04, 0x00, 0x01, 0x02, 0x77, 0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31,
        0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71, 0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91, 0xa1, 0xb1, 0xc1, 0x09,
        0x23, 0x33, 0x52, 0xf0, 0x15, 0x62, 0x72, 0xd1, 0x0a, 0x16, 0x24, 0x34, 0xe1, 0x25, 0xf1, 0x17, 0x18, 0x19, 0x1a,
        0x26, 0x27, 0x28, 0x29, 0x2a, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a,
        0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x73, 0x74, 0x75,
        0x76, 0x77, 0x78, 0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x92, 0x93, 0x94, 0x95, 0x96,
        0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7,
        0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8,
        0xd9, 0xda, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9,
        0xfa, 0xff, 0xda, 0x00, 0x0c, 0x03, 0x01, 0x00, 0x02, 0x11, 0x03, 0x11, 0x00, 0x3f, 0x00, 0xf9, 0xfe, 0x8a, 0x28,
        0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a,
        0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02,
        0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0,
        0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28,
        0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a, 0x28, 0xa0, 0x02, 0x8a,
        0x28, 0xa0, 0x0f, 0xff, 0xd9
    ]

    def _convert_key_num_to_device_key_id(self, key):
        return self.KEY_NUM_TO_DEVICE_KEY_ID[key]
    
    def _convert_device_key_id_to_key_num(self, key):
        return self.KEY_DEVICE_KEY_ID_TO_NUM[key]
    
    
    def _make_payload_for_report_id(self, report_id, payload_data):
        payload = bytearray(self.PACKET_LENGHT + 1)
        payload[0] = report_id
        payload[1:len(payload_data)] = payload_data
        return payload

    def _read_control_states(self):
        states = [False] * self.KEY_COUNT

        # _key_triggered_last_read exists since 293S only triggers an HID event when a button is released.
        # there are no key down and key up events, so we have to simulate the key being pressed and released.
        # if a firmware upgrade that supports key down/up events is released, this variable can be removed from the code.

        if not self._key_triggered_last_read:
            device_input_data = self.device.read(self.PACKET_LENGHT)
            if device_input_data is None:
                return None
            
            if(device_input_data.startswith(bytes([0x41, 0x43, 0x4b, 0x00, 0x00, 0x4f, 0x4b, 0x00]))): # ACK\0\0OK\0
                triggered_key = self._convert_device_key_id_to_key_num(int.from_bytes(device_input_data[9:10], 'big', signed=False))            
            else:
                # we don't know how to handle the response
                return None
            
            states = [False] * self.KEY_COUNT
            states[triggered_key] = True
            self._key_triggered_last_read = True
        else:
            self._key_triggered_last_read = False

        return {
            ControlType.KEY: states
        }

    def _reset_key_stream(self):
        self.reset()

    def reset(self):
        # disconnect # CRT\0\0DIS
        payload = self._make_payload_for_report_id(0x00, [0x43, 0x52, 0x54, 0x00, 0x00, 0x44, 0x49, 0x53])
        self.device.write(payload)

        # connect/ping # CRT\0\0CONNECT
        payload = self._make_payload_for_report_id(0x00, [0x43, 0x52, 0x54, 0x00, 0x00, 0x43, 0x4f, 0x4e, 0x4e, 0x45, 0x43, 0x54])
        self.device.write(payload)

        # clear contents # CRT\0\0CLE #0x00 0x00 0x00 <KEY ID | 0xff for all>
        payload = self._make_payload_for_report_id(0x00, [0x43, 0x52, 0x54, 0x00, 0x00, 0x43, 0x4c, 0x45, 0x00, 0x00, 0x00, 0xff])
        self.device.write(payload)

    def set_brightness(self, percent):
        if isinstance(percent, float):
            percent = int(100.0 * percent)

        percent = min(max(percent, 0), 100)

        # set brightness # CRT\0\0LIG #0x00 0x00 <PERCENT> 0x00
        payload = self._make_payload_for_report_id(0x00, [0x43, 0x52, 0x54, 0x00, 0x00, 0x4c, 0x49, 0x47, 0x00, 0x00, percent, 0x00])
        self.device.write(payload)

    def get_serial_number(self):
        return self.device.serial_number()

    def get_firmware_version(self):
        version = self.device.read_input(0x00, self.PACKET_LENGHT + 1)
        return self._extract_string(version[1:])

    def set_key_image(self, key, image):
        if min(max(key, 0), self.KEY_COUNT) != key:
            raise IndexError("Invalid key index {}.".format(key))

        image = bytes(image or self.BLANK_KEY_IMAGE)
        image_payload_page_length = self.PACKET_LENGHT

        key = self._convert_key_num_to_device_key_id(key)

        image_size_uint16_be = int.to_bytes(len(image), 2, 'big', signed=False)

        # start batch # CRT\0\0BAT #0x00 0x00 <image size uint16_be> <key id>
        command = bytes([0x43, 0x52, 0x54, 0x00, 0x00, 0x42, 0x41, 0x54, 0x00, 0x00]) + image_size_uint16_be +  bytes([key]) 
        payload = self._make_payload_for_report_id(0x00, command)
        self.device.write(payload)

        page_number = 0
        bytes_remaining = len(image)
        while bytes_remaining > 0:
            this_length = min(bytes_remaining, image_payload_page_length)
            bytes_sent = page_number * image_payload_page_length

            #send data
            payload = self._make_payload_for_report_id(0x00, image[bytes_sent:bytes_sent + this_length])
            self.device.write(payload)

            bytes_remaining = bytes_remaining - this_length
            page_number = page_number + 1
        
        # stop batch # CRT\0\0STP
        payload = self._make_payload_for_report_id(0x00, [0x43, 0x52, 0x54, 0x00, 0x00, 0x53, 0x54, 0x50])
        self.device.write(payload)
        


    def set_touchscreen_image(self, image, x_pos=0, y_pos=0, width=0, height=0):
        pass
