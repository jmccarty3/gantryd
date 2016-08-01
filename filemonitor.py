#Importing a polling observer to account for docker mounting issues
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
import os

class FileMonitor(FileSystemEventHandler):
    def __init__(self, file, action):
        self.path,self.filename = os.path.split(file)
        self.action = action
        self.observer = None
    def start(self):
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=False)
        self.observer.start()
    def stop(self):
        if self.observer is not None:
            self.observer.stop()
    def join(self):
        if self.observer is not None:
            self.observer.join()

    def on_modified(self, event):
        try:
            if os.path.samefile(event.src_path,self.filename):
                self.action()
        except OSError as e:
            print 'Exception on file check', e
