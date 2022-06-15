import compose
import data
import input
import parse


# TODO: need to add logging
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
    # output.print_text(output_data)


if __name__ == "__main__":
    main()
