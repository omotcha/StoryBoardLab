import os
import json
from json.decoder import JSONDecodeError


class Page:
    def __init__(self, page_dict: dict):
        """
        load page dictionary into pyobj
        :param page_dict:
        """
        self.start_tick = page_dict["start_tick"]
        self.end_tick = page_dict["end_tick"]
        self.scan_line_direction = page_dict["scan_line_direction"]


if __name__ == '__main__':
    pass
