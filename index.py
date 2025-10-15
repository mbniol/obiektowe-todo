import modules.objectLib as ol
from classes.Priority import Priority
from classes.EditType import EditType
from web.webHost import app
import threading
import webbrowser
import time


def runApp():
    app.run()
    
def runBrowser():
    url = "http://127.0.0.1:5000"
    webbrowser.open(url,new=0, autoraise=True)


if __name__ == "__main__":
    thread_run_app = threading.Thread(target=runApp)
    thread_run_app.daemon = True


    thread_run_app.start()
    print("App thread started")

    runBrowser()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Zamykanie programu...")