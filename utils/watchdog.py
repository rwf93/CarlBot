import os 
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# fucking scuffed as shit
class Watchdog(FileSystemEventHandler):
    def __init__(self, watcher) -> None:
        super().__init__()
        self.watcher = watcher
    
    file_cache = {}

    def on_modified(self, event):
        seconds = int(time.time())
        key = (seconds, event.src_path)
        if key in self.file_cache:
            return
        self.file_cache[key] = True

        self.watcher(event.src_path)

def setup_watchdog(watcher, path):
    observer = Observer()
    observer.schedule(Watchdog(watcher=watcher), path, recursive=False)
    observer.start()

    return observer

def kill_watchdog(observer):
    observer.stop()
    observer.join()