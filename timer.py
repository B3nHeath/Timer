#!/usr/bin/python3
from datetime import datetime
import time
import subprocess, sys
import os
import re
import threading

def main():
    # Collect timer length
    length = (float(input("Timer (minutes): "))*60)
    print("Start")
    # Create our timer thread
    timer_thread = threading.Thread(target = timer, args = (length,))
    # Start timer thread in background
    timer_thread.start()
    # Collect start time
    start = time.time()
    # If timer is still working
    while timer_thread.is_alive():
        prog = input("Progress? ")
        # if you want progress update
        if prog == "Y":
            # Print amount of time elapsed
            print(f"Time elapsed: {(time.time() - start)/60 :.1f} minutes")
    

def timer(length):
    # Extract today's date in the desired format
    today = datetime.today().strftime('%Y-%m-%d')
    # Do you want to write work into daily notes?
    write_to_file = '-w' in sys.argv
    # sleep function for desired time
    time.sleep(length)

    # Open finished notice
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, "/home/ben/Python/Projects/Timer/timer.pdf"])

    # If you want to add to file
    if write_to_file:
        reason = input("Work type: ")
        # Path to daily note
        file_path = os.path.expanduser(f"~/Notes/Obsidian_notes/Journal/Daily_notes/{today}.md")
        # Empty storage for text
        text = []

        # Append document to text
        with open(file_path, "r") as file:
            for line in file:
                text.append(line)

        found_heading = False
        done = False
        # For each line in text
        for pos, line in enumerate(text):
            # If you have found the work heading and job is not done
            if found_heading and not done:
                # Find first line that doesn't start as whitespace -> a dash
                if not re.fullmatch(r"\s*-.*\n", line):
                    # Insert our work record in this position in the document
                    text.insert(pos, f"- {int(length/60)} - {reason}\n")
                    # Completed desired function
                    done = True

            # If you haven't found the relevant heading yet, look for it
            if not found_heading:
                if line == '### Work Record:\n':
                    found_heading = True

        # Write the updated file
        with open(file_path, "w") as file:
            for line in text:
                file.write(line)

        # End the program
        sys.exit()

if __name__ == "__main__":
    main()