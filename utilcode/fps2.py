#!/bin/python
import time
from utility import fps_counter

@fps_counter
def process_frame():
    time.sleep(0.02)  # Simulate work
    return "Frame Processed"

for _ in range(5):
    result, fps = process_frame()
    print(f"{result}, FPS = {fps:.1f}")
