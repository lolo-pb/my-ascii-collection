#!/usr/bin/env python3
import argparse
import sys
import time
from pathlib import Path

FRAME_FILE = Path(__file__).with_name("hands.txt")


def load_frames(path):
    frames = []
    current = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "#":
            if current:
                frames.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        frames.append("\n".join(current))
    return frames


def main():
    parser = argparse.ArgumentParser(description="Animate ASCII frames from hands.txt")
    parser.add_argument("-d", "--delay", type=float, default=0.25, help="seconds between frames")
    parser.add_argument("-n", "--loops", type=int, default=0, help="number of loops (0 = infinite)")
    args = parser.parse_args()

    frames = load_frames(FRAME_FILE)
    if not frames:
        sys.exit(f"No frames found in {FRAME_FILE}")

    print("\033[?25l", end="", flush=True)
    try:
        loop = 0
        while args.loops == 0 or loop < args.loops:
            for frame in frames:
                print("\033[H" + frame + "\033[J", end="", flush=True)
                time.sleep(args.delay)
            loop += 1
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h\033[0m", flush=True)


if __name__ == "__main__":
    main()
