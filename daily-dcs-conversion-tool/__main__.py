import compose
import input
import output
import parse
from model import data_model


# TODO: add deployment settings
# TODO: add logging
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
    output.print_text_as_csv(output_data)


if __name__ == "__main__":
    main()
