import key


# compose parsed_data into output_data
def compose_output_text(parsed_data, output_data) -> []:
    # keyword part
    __compose_keyword_part(parsed_data.available_keywords, parsed_data.key_data
                           , parsed_data.key_orig_texts, output_data.keyword_part)

    # memo part
    __compose_memo_part(parsed_data.memo_data, output_data.memo_part)


# compose keyword part
def __compose_keyword_part(available_keywords, key_data, key_orig_texts, keyword_part):
    # first, set a header row
    __compose_keyword_header_row(available_keywords, keyword_part)

    # TODO: add error handling and logging
    # iterate by date (each row consists of data for each date)
    for current_date in range(1, len(key_data) + 1):
        keyword_part[current_date] = [current_date]  # first column is date

        # loop by entire KEYWORDS to keep the order or keywords
        for keyword in key.KEYWORDS:
            # append data of keywords exist in this month
            if keyword in available_keywords:
                # check if keyword exists on current date
                if key_data[current_date].get(keyword):
                    sum_data = key_data[current_date][keyword]
                    if sum_data.is_integer():
                        sum_data = int(sum_data)

                    keyword_part[current_date].append(sum_data)
                    keyword_part[current_date].append(' '.join(key_orig_texts[current_date][keyword]))
                # keyword does not exist on current date
                else:
                    keyword_part[current_date].append('')
                    keyword_part[current_date].append('')  # append blank twice


# compose a header row of keyword part
def __compose_keyword_header_row(available_keywords, keyword_part):
    keyword_part[0] = ['date']  # first column is date

    for keyword in key.KEYWORDS:
        if keyword in available_keywords:
            keyword_part[0].append(keyword)  # key sum data column
            keyword_part[0].append(keyword + '-detail')  # key orig text data column


# compose memo part
def __compose_memo_part(memo_data, memo_part):
    for current_date in memo_data.keys():
        for memo_line in memo_data[current_date]:
            # memo_part has only two columns (date, memo)
            memo_part.append((current_date, ' '.join(memo_line)))
