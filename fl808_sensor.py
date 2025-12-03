#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2023 Kent Gibson <warthog618@gmail.com>

"""Minimal example of watching for rising edges on a single line."""

import gpiod
from gpiod.line import Edge
import time
import queue

TOTAL_RUNTIME = 2  # seconds
counts_per_litre = 334



def watch_line_rising(chip_path, line_offset):
    start_time = time.time()
    count = 0
    with gpiod.request_lines(
        chip_path,
        consumer="watch-line-rising",
        config={line_offset: gpiod.LineSettings(edge_detection=Edge.RISING)},
    ) as request:
        while (time.time() < start_time + TOTAL_RUNTIME):
            # Blocks until at least one event is available
            for event in request.read_edge_events():
                #print("line: {}  type: Rising   event #{}".format(event.line_offset, event.line_seqno))
                count += 1

    #print(f"\nTotal rising edges detected: {count} in {TOTAL_RUNTIME} seconds")
    frequency = count / TOTAL_RUNTIME
    flow_rate = (frequency / counts_per_litre) * 60  # Liters per minute
    return flow_rate  # Liters per minute

def read_fl808_thread(chip_path, line_offset, fl808_queue):
    while True:
        try:
            flow_rate = watch_line_rising(chip_path, line_offset)
            fl808_queue.put(flow_rate)

        except KeyboardInterrupt:
            break