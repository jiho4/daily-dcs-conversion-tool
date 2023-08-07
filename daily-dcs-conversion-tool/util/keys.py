import yaml

with open('resources/config.yml') as f:
    __conf = yaml.safe_load(f)

# const keywords
KEYWORDS = tuple(__conf['keywords'].split(', '))
INT_KEYWORDS = tuple(__conf['int_keywords'].split(', '))
