import os
from datetime import datetime
from logging import getLogger, config

import yaml

import compose
import input
import parse
import print
from model import data_model

with open('resources/log_config.yaml', 'r') as f:
    __log_conf = yaml.safe_load(f)

log_dir = __log_conf['log_directory']
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

__log_conf['handlers']['fileHandler']['filename'] = \
    log_dir + '/app.log.{}'.format(datetime.now().strftime('%Y%m%d'))
config.dictConfig(__log_conf)
logger = getLogger(__name__)


# TODO: add test
# TODO: add error handling
def main():
    # declare model classes
    parsed_data = data_model.ParsedData()
    output_data = data_model.OutputData()

    # get input data
    daily_text = input.input_string()

    # parse input data
    parse.parse_daily_text(daily_text, parsed_data)

    # compose parsed data
    compose.compose_output_text(parsed_data, output_data)

    # print composed data
    print.print_text_as_csv(output_data)


if __name__ == "__main__":
    logger.info('Application started')
    main()
