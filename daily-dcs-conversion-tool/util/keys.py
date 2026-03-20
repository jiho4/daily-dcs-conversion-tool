import os
import yaml

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'config.yaml')

with open(_CONFIG_PATH) as f:
    __conf = yaml.safe_load(f)

# const keywords
KEYWORDS = tuple(__conf['keywords'].split(', '))
INT_KEYWORDS = tuple(__conf['int_keywords'].split(', '))


def load_keywords_from_config(config_path: str):
    """Load keywords from a custom config file."""
    with open(config_path) as f:
        conf = yaml.safe_load(f)
    keywords = tuple(conf['keywords'].split(', '))
    int_keywords = tuple(conf['int_keywords'].split(', '))
    return keywords, int_keywords
