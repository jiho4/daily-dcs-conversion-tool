import os
from datetime import datetime
from logging import getLogger, config

import yaml

import compose
import reader
import parse
import writer
from model import data_model

_LOG_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'log_config.yaml')

with open(_LOG_CONFIG_PATH, 'r') as f:
    __log_conf = yaml.safe_load(f)

log_dir = __log_conf['log_directory']
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

__log_conf['handlers']['fileHandler']['filename'] = \
    log_dir + '/app.log.{}'.format(datetime.now().strftime('%Y'))
config.dictConfig(__log_conf)
logger = getLogger(__name__)


def main():
    # declare model classes
    parsed_data = data_model.ParsedData()
    output_data = data_model.OutputData()

    # get input data
    daily_text = reader.input_string()
    logger.info('Input text has %d lines', len(daily_text))

    # parse input data
    parse.parse_daily_text(daily_text, parsed_data)

    # compose parsed data
    compose.compose_output_text(parsed_data, output_data)

    # print composed data
    writer.print_text_as_csv(output_data)


if __name__ == "__main__":
    logger.info('Application started')
    main()
