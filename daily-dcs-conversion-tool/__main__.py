import compose
import data
import input
import output
import parse


# TODO: toFix) error occurs when there is a blank line at the start
# TODO: sometimes linefeed is not working. better to convert all possible linefeed in input.py
# TODO: add env for config.yml (dev, prod)
# TODO: add deployment settings
# TODO: add logging
# TODO: add test
# TODO: add error handling
def main():
    # declare model classes
    parsed_data = data.ParsedData()
    output_data = data.OutputData()

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
