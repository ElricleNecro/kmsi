#!/usr/bin/env python
# encoding: utf-8

from hid import device
from . import constants as c
from . import exception as e


class Device(object):
    def __init__(self, vendor_id, product_id, config=None):
        self._vid = vendor_id
        self._pid = product_id

        self._device = device()
        try:
            self._device.open(self._vid, self._pid)
        except IOError:
            raise IOError("Unable to open device (%x, %x)" % (self._vid, self._pid))

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

        self.setColor("left", **self._config["left"])
        self.setColor("middle", **self._config["middle"])
        self.setColor("right", **self._config["right"])
        self.setMode(self._config["mode"])

    def sendRequest(self, req):
        ret = self._device.send_feature_report(req)
        if ret == -1:
            raise e.SendError(self._device.error(), ret, self._config)

    def setColor(self, region, color, level="high"):
        self._config[region]["color"] = color
        self._config[region]["level"] = level

        buf = [0] * 8

        buf[0] = 1
        buf[1] = 2
        buf[2] = 66
        buf[3] = c.REGIONS[region]
        buf[4] = c.COLORS[color]
        buf[5] = c.LEVELS[level]
        buf[6] = 0
        buf[7] = 236

        self.sendRequest(buf)

    def setMode(self, mode):
        self._config["mode"] = mode

        buf = [0] * 8

        buf[0] = 1
        buf[1] = 2
        buf[2] = 65
        buf[3] = c.MODES[mode]
        buf[4] = 0
        buf[5] = 0
        buf[6] = 0
        buf[7] = 236

        self.sendRequest(buf)

    def __del__(self):
        self._device.close()
