from util import keys


# compose parsed_data into output_data
def compose_output_text(parsed_data, output_data) -> []:
    keyword_value = {}   # {kw: {date: value}} — available keywords only
    keyword_detail = {}  # {kw: {date: detail_text}} — available keywords only
    num_dates = len(parsed_data.key_data)

    # flatten key_data and key_orig_texts into keyword_value and keyword_detail dicts
    for current_date in range(1, num_dates + 1):
        # collect each keyword's sum and original text for the current date
        for keyword in parsed_data.key_data[current_date]:
            sum_data = parsed_data.key_data[current_date][keyword]
            if sum_data.is_integer():
                sum_data = int(sum_data)
            keyword_value.setdefault(keyword, {})[current_date] = sum_data
            keyword_detail.setdefault(keyword, {})[current_date] = ' '.join(
                parsed_data.key_orig_texts[current_date][keyword])

    _compose_no_detail_part(parsed_data.available_keywords, keyword_value, num_dates, output_data.all_key_data_part)
    _compose_keyword_detail_part(parsed_data.available_keywords, keyword_value, keyword_detail, num_dates,
                                 output_data.keyword_detail_part)
    _compose_memo_part(parsed_data.memo_data, output_data.memo_part)


# compose no-detail part: all keywords as columns, values only
def _compose_no_detail_part(available_keywords, keyword_value, num_dates, no_detail_part):
    no_detail_part.append(['date'] + list(keys.KEYWORDS))
    # one row per date: fill blank for keywords not present this month
    for date in range(1, num_dates + 1):
        row = [date] + [keyword_value[kw].get(date, '') if kw in available_keywords else ''
                        for kw in keys.KEYWORDS]
        no_detail_part.append(row)


# compose keyword-detail part: available keywords only, with value and detail columns interleaved
def _compose_keyword_detail_part(available_keywords, keyword_value, keyword_detail, num_dates, keyword_detail_part):
    available = [kw for kw in keys.KEYWORDS if kw in available_keywords]
    header = ['date'] + [col for kw in available for col in (kw, kw + '-detail')]
    keyword_detail_part.append(header)
    # one row per date: interleave value and detail columns for each available keyword
    for date in range(1, num_dates + 1):
        row = [date] + [x for kw in available
                        for x in (keyword_value[kw].get(date, ''), keyword_detail[kw].get(date, ''))]
        keyword_detail_part.append(row)


# compose memo part
def _compose_memo_part(memo_data, memo_part):
    # iterate each date that has memo entries
    for current_date in memo_data.keys():
        # join multi-token memo lines into a single string per row
        for memo_line in memo_data[current_date]:
            memo_part.append((current_date, ' '.join(memo_line)))
