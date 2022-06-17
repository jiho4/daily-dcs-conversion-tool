# get the whole daily_text of a month and return it as a list of lines
def input_string():
    daily_text = []  # store a daily text line by line

    print("* Paste the entire daily text, and press Cmd+D or Ctrl-D or Ctrl-Z ( windows ) to commit.")
    while True:
        try:
            line = input()
        except EOFError:
            break
        # trim each lines
        daily_text.append(line.strip())
    return daily_text
