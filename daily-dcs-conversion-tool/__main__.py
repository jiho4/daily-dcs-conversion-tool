import compose
import data
import input
import parse


def main():
    d = data.Data()

    daily_text = input.input_string()

    parse.parse_daily_text(daily_text, d)

    compose.compose_output_text(d)

    # Output.print_text


if __name__ == "__main__":
    main()
