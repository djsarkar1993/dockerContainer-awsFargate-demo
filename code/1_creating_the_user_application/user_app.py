# Imports
import os
import time
import logging
import pandas as pd




# Main
if __name__ == '__main__':
    # Setting up the logger
    log_stream_name = 'user-app'
    msg_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    datetime_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=msg_format, datefmt=datetime_format)
    logger = logging.getLogger(log_stream_name)
    logger.setLevel(logging.INFO)
    logger.info("Logger setup successful!")


    # Reading the runtime arguments from the OS environment
    runtime_args = eval(os.environ.get('RUNTIME_ARGS', '{}'))
    logger.info(f'The input arguments are: {runtime_args}')


    # Waiting for 30 seconds
    logger.info('Waiting for 30 seconds... ... ...')
    time.sleep(30)


    # Displaying the contents of the runtime arguments as a pandas dataframe
    df = pd.DataFrame(runtime_args)
    logger.info(f'Displaying the contents of the runtime arguments as a pandas dataframe:\n{df}')
