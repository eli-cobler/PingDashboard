import time
import setup
import text
import logging

def start():
    while True:
        try:
            setup.run()             # runs setup and saves location dict locally
            #TODO Remove print statement and change time to 60 instead of 5
            print("Waiting 5 secs...")
            time.sleep(5)           # pauses for 60 seconds before running backend script again
        except UnboundLocalError:
            #text.send()
            logging.basicConfig(filename='timer.log', 
                                format='%(asctime)s %(message)s', 
                                datefmt='%m/%d/%Y %I:%M:%S %p', 
                                level=logging.DEBUG)
            logging.info('UnboundLocalError')
            logging.info('The timer was restarted.')

if __name__ == '__main__':
    start()