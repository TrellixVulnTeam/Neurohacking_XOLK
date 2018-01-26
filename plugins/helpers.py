# -*- coding: utf-8 -*-
"""
Project: neurohacking
File: helpers.py
Author: wffirilat
"""

import numpy as np

import plugin_interface as plugintypes
from open_bci_v3 import OpenBCISample

class PluginHelpers(plugintypes.IPluginExtended):
    def __init__(self):
        self.packetnum = -1
        self.ticknum = None
        self.storelength = 1024
        self.rawdata = np.zeros((8, self.storelength))
        self.data = np.zeros((8, self.storelength))

    def activate(self):
        print("helpers activated")

    # called with each new sample
    def __call__(self, sample: OpenBCISample):
        if sample.id == 0:
            self.packetnum += 1
        self.rawdata[:, (sample.id + 256 * self.packetnum) % self.storelength] = sample.channel_data
        self.data[:, (sample.id + 256 * self.packetnum) % self.storelength] = [v - avg for avg, v in zip(
            [sum(self.rawdata[i, :]) / self.storelength for i in range(8)],
            sample.channel_data
        )]
        self.print(sample)

    def minmax(self, sample):
        print(min(self.data[3, :]), max(self.data[3, :]))

    def print(self, sample):
        print(self.data[3,-1])

    def thresholdDetect(self, sample):
        if self.data[3, (sample.id + 256 * self.packetnum) % self.storelength] > 1000:
            print((sample.id + 256 * self.packetnum))