def input_string():
    daily_text = []
    print("* Paste the entire daily text, and press Cmd+D or Ctrl-D or Ctrl-Z ( windows ) to commit.")
    while True:
        try:
            line = input()
        except EOFError:
            break
        # trim each lines
        daily_text.append(line.strip())
    return daily_text
