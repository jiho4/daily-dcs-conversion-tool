import key


def compose_output_text(parsed_data, output_data) -> []:
    __compose_keyword_part(parsed_data.key_data, parsed_data.key_orig_texts, output_data.keyword_part)

    __compose_memo_part(parsed_data.memo_data, output_data.memo_part)


def __compose_keyword_part(key_data, key_orig_texts, keyword_part):
    __compose_keyword_header_row(keyword_part)

    # TODO: add error handling and logging
    # iterate by date (each row consists of data for each date)
    for current_date in range(1, len(key_data)):
        keyword_part[current_date] = [current_date]

        for keyword in key.KEYWORDS:
            # check if keyword exists in key_data of current date
            if key_data[current_date].get(keyword):
                sum_data = key_data[current_date][keyword]
                if sum_data.is_integer():
                    sum_data = int(sum_data)

                keyword_part[current_date].append(sum_data)
                keyword_part[current_date].append(' '.join(key_orig_texts[current_date][keyword]))
            else:
                keyword_part[current_date].append('')
                keyword_part[current_date].append('')  # append blank twice


def __compose_keyword_header_row(keyword_part):
    keyword_part[0] = ['date']

    for keyword in key.KEYWORDS:
        keyword_part[0].append(keyword)
        keyword_part[0].append(keyword + 'detail')


def __compose_memo_part(memo_data, memo_part):
    for current_date in memo_data.keys():
        for memo_line in memo_data[current_date]:
            # memo_part has only two columns (date, memo)
            memo_part.append((current_date, ' '.join(memo_line)))
