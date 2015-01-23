#!/usr/bin/env python
# encoding: utf-8


""".. hid::
    This module contains the Device class. It allow users to modify keyboard
    mode and lightning.
"""


from hid import device
from . import constants as c
from . import exception as e


class Device(object):
    """.. class:: Device(vendor_id, product_id[, config=None])
        This class take the keyboard identifier, and set up an interface which
        allow "easy" modifying of mode and lighting.

        :param vendor_id: vendor identifier
        :type vendor_id: int
        :param product_id: product id
        :type product_id: int
        :param config: default configuration
        :type config: dict or None
    """
    def __init__(self, vendor_id, product_id, config=None):
        self._vid = vendor_id   #Keyboard vendor id (6000 for MSI)
        self._pid = product_id  #Keyboard id (65280 for MSI gaming keyboard)

        # Creating the device instance:
        self._device = device()
        # And opening the wanted one:
        try:
            self._device.open(self._vid, self._pid)
        except IOError:
            raise IOError("Unable to open device (%x, %x)" % (self._vid, self._pid))

        # Loading the default configuration:
        if config is not None:
            self._config = config
        else:
            self._config = dict(
                mode="normal",
                left=dict(
                    color="red",
                    level="high",
                ),
                middle=dict(
                    color="sky",
                    level="high",
                ),
                right=dict(
                    color="purple",
                    level="high",
                )
            )

    def update(self):
        """.. classmethod:: update()
            Force updating keyboard properties.
        """
        self.setColor("left", **self._config["left"])
        self.setColor("middle", **self._config["middle"])
        self.setColor("right", **self._config["right"])
        self.setMode(self._config["mode"])

    def sendRequest(self, req):
        """.. classmethod:: sendRequest(req)
            Send a feature request to the keyboard.

            :param req: a array of integer between 1 and 255.
            :type req: list
        """
        ret = self._device.send_feature_report(req)
        if ret == -1:
            raise e.SendError(self._device.error(), ret, self._config)

    def setColor(self, region, color, level="high"):
        """.. classmethod:: setColor(region, color[, level="high"])
            Set `color` of the designated `region`.

            :param region: region to colorize.
            :type region: str
            :param color: color to use.
            :type color: str or int
            :param level: Intensity level of the region ("low", "med", "high", "off").
            :type level: str
        """
        # Update the config dictionary:
        self._config[region]["color"] = color
        self._config[region]["level"] = level

        # Creation of the buffer containing the request
        buf = [0] * 8

        buf[0] = 1
        buf[1] = 2
        buf[2] = 66                 # indicating a set request
        buf[3] = c.REGIONS[region]
        buf[4] = c.COLORS[color]
        buf[5] = c.LEVELS[level]
        buf[6] = 0
        buf[7] = 236                # EOR (end of request)

        # Sending the request:
        self.sendRequest(buf)

    def setMode(self, mode):
        """.. classmethod:: setMode(mode)
            Set the mode of the keyboard ("normal", "gaming", "breathe", "demo", "wave")

            :param mode: mode to use
            :type mode: str
        """
        # Update the config dictionary:
        self._config["mode"] = mode

        # Creation of the buffer containing the request
        buf = [0] * 8

        buf[0] = 1
        buf[1] = 2
        buf[2] = 65                 # indicating a commit request
        buf[3] = c.MODES[mode]
        buf[4] = 0
        buf[5] = 0
        buf[6] = 0
        buf[7] = 236                # EOR (end of request)

        # Sending the request:
        self.sendRequest(buf)

    def __del__(self):
        # closing properly the device:
        self._device.close()
