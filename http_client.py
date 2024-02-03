import http.client, threading, time
from sys import argv

#threaded loop to send 
def loadMixPreset(mixes, timeout, stop):
    conn = http.client.HTTPConnection('127.0.0.1:40512')
    while True:
        # load in a preset for each layer on each mix
        for mix in range(1, mixes + 1):
            conn.request("GET", f"/mix/{mix}/preset/1")
            r1 = conn.getresponse()
            print(f'Mix: {mix} preset: 1 - {r1.status}, {r1.reason}')
            r1.read()
            if stop():
                print("Exiting Loop")
                break
            time.sleep(timeout)
        
        # load in a reset preset
        for mix in range(1, mixes + 1):
            conn.request("GET", f"/mix/{mix}/preset/2")
            r1 = conn.getresponse()
            print(f'Mix: {mix} preset: 2 - {r1.status}, {r1.reason}')
            r1.read()
            if stop():
                print("Exiting Loop")
                break
            time.sleep(timeout)

def loadLayerPreset(mixes, timeout, stop):
    conn = http.client.HTTPConnection('127.0.0.1:40512')
    while True:
        # load in a preset for each layer on each mix
        for mix in range(1, mixes + 1):
            for i, layer in enumerate(range(1, 5)):
                conn.request("GET", f"/mix/{mix}/layer/{layer}/preset/{i+1}")
                r1 = conn.getresponse()
                print(f'Mix: {mix} Layer: {layer} preset: {i+1} - {r1.status}, {r1.reason}')
                r1.read()
                if stop():
                    print("Exiting Loop")
                    break
                time.sleep(timeout)
        
            # load in a reset preset
        for mix in range(1, mixes + 1):
            for layer in range(1, 5):
                # preset [0,5] is the reset layer
                conn.request("GET", f"/mix/{mix}/layer/{layer}/preset/5")
                r1 = conn.getresponse()
                print(f'Mix: {mix} Layer: {layer} preset: 5 - {r1.status}, {r1.reason}')
                r1.read()
                if stop():
                    print("Exiting Loop")
                    break
                time.sleep(timeout)

def options():
    print(
        """
        ---------------------------------------------------------
        REST API STRESS TEST
        ---------------------------------------------------------

        This script will run a stress test on the REST web server.
        The webserver url is http://localhost:40512

        !!!!! Each MIX must be configured with 4 LAYERS !!!!!

        The test will load a mix preset onto each mix, followed by a reset preset.

        A LayerPreset in slot [0,0] will be loaded into each layer of a 4-layer mix
        loading a clip from slot [10,10] onto each layer and transforming
        the clip into a quadrant of the mix.

        Each layer on each mix is then reset.

        The process continues until the window is closed or 'q' is entered, closing the loop
        ready to be started again.

        COMMAND LINE ARGUMENTS
        ----------------------------------------------------------
        -t = token to read the args
        mixes = integer value of total mixes
        wait - time in ms between each request 

        """
    )

def stdinput():
    try:
        mixes = int(input('Enter the number of mixes to stress test:>\n'))
    except ValueError:
        print('input value is not valid')
        stdinput()

    except (KeyboardInterrupt, SystemExit):
        print('Forced exit')
        raise

    try:
        timeout = float(input('Enter the length of wait before each request in ms:>\n'))
    except ValueError:
        print('input value is not valid\n')
        stdinput()
    except (KeyboardInterrupt, SystemExit):
        print('Forced exit\n')
        raise

    try:
        uip = str(input('Enter the test to run (Mixes/layer) stress test.'))
        if uip not in ('mixes', 'layer'):
            raise ValueError
        if uip == 'mixes':
            test = 'mixes'
        if uip == 'layer':
            test = 'layer'
    except ValueError:
        print('input value is not valid\n')
        stdinput()
    except (KeyboardInterrupt, SystemExit):
        print('Forced exit\n')
        raise
    return mixes, timeout, test

def parse_arguments():
    if argv[1] != '-t':
        print('''
            Invalid argument passed,
            arg[1] should equal -t
            arg[2] should equal number of mixes (int) 
            arg[3] should equal wait time in seconds between requests (float)
            arg[4] choose the test you would like to run mix or layer (string)''')
        quit()
    else:
        if argv[2]:
            mixes = int(argv[2])
        if argv[3]:
            timeout = float(argv[3])    
        if argv[4]:
            test = str(argv[4])    
        return mixes, timeout, test

def launch_test(test, mixes, timeout):
    stop_threads = False

    if test == 'mixes':
        thread = threading.Thread(
            target=loadMixPreset,
            args=(mixes, timeout, lambda: stop_threads),
            daemon=True)

    if test == 'layers':
        thread = threading.Thread(
            target=loadLayerPreset,
            args=(mixes, timeout, lambda: stop_threads),
            daemon=True)
    return thread


def main():
    if __name__ == "__main__":
        # Check if command line arguments are passed and if so set the mixes and timeout values accordingly
        mixes = None
        timeout = None
        test = None
        if len(argv) > 1:
            mixes, timeout, test = parse_arguments()
        else:
            options()
            mixes, timeout, test = stdinput()
        
        # start threaded task via launch test option parsing
        thread = launch_test(test, mixes, timeout)
        thread.start()
    
        close = False
        while not close:
            i = input("Press 'q' to close.\n")
            if i == 'q':
                close = True

main()