import os
import json
from json.decoder import JSONDecodeError
from configs.common import example_dir


class Page:
    def __init__(self, page_dict: dict):
        """
        load page dictionary into pyobj
        :param page_dict:
        """
        self.start_tick = page_dict["start_tick"]
        self.end_tick = page_dict["end_tick"]
        self.scan_line_direction = page_dict["scan_line_direction"]


class Tempo:
    def __init__(self, tempo_dict: dict):
        """
        load tempo dictionary into pyobj
        :param tempo_dict:
        """
        self.tick = tempo_dict["tick"]
        self.value = tempo_dict["value"]


class Note:
    def __init__(self, note_dict: dict):
        """
        load note dictionary into pyobj
        :param note_dict:
        """
        self.page_index = note_dict["page_index"]
        self.type = note_dict["type"]
        self.id = note_dict["id"]
        self.tick = note_dict["tick"]
        self.x = note_dict["x"]
        self.has_sibling = note_dict["has_sibling"]
        self.hold_tick = note_dict["hold_tick"]
        self.next_id = note_dict["next_id"]
        self.is_forward = note_dict["is_forward"]


class Event:
    def __init__(self, event_dict: dict):
        """
        load event
        :param event_dict:
        """
        self.tick = event_dict["tick"]
        self.event_list = event_dict["event_list"]


class Chart:
    def __init__(self, chart_json: str):
        """
        load json-format chart's content into a dictionary then into pyobj
        :param chart_json: chart file name(str)
        """

        # load chart json
        _, ext = os.path.splitext(chart_json)
        if ext != ".json":
            raise (Exception("FileError: Not a valid chart file format: {}.".format(ext)))
        try:
            with open(chart_json, "r") as f:
                chart_dict = json.load(f)
        except FileNotFoundError:
            print("FileError: No such chart file: {}.".format(chart_json))
            return
        except JSONDecodeError:
            print("JSONError: Bad chart content: {}.".format(chart_json))
            return

        # parse the metadata
        self.format_version = chart_dict["format_version"]
        self.time_base = chart_dict["time_base"]
        self.start_offset_time = chart_dict["start_offset_time"]

        # parse pages, tempos, notes and events
        self.page_list = []
        self.tempo_list = []
        self.note_list = []
        self.event_order_list = []
        for page in chart_dict["page_list"]:
            self.page_list.append(Page(page))
        for tempo in chart_dict["tempo_list"]:
            self.tempo_list.append(Tempo(tempo))
        # add a tail to the tempo list
        self.tempo_list.append(Tempo({"tick": self.get_max_tick(), "value": -1}))
        for note in chart_dict["note_list"]:
            self.note_list.append(Note(note))
        for events in chart_dict["event_order_list"]:
            self.event_order_list.append(Event(events))

        # calculate max time
        self.max_time = 0
        for tid in range(len(self.tempo_list) - 1):
            self.max_time += (self.tempo_list[tid + 1].tick - self.tempo_list[tid].tick) * \
                             self.tempo_list[tid].value / 1000000 / self.time_base

    def get_max_tick(self):
        return self.page_list[-1].end_tick


def test():
    nhelv = os.path.join(example_dir, "nhelv.json")
    chart = Chart(nhelv)
    print(len(chart.page_list))


if __name__ == '__main__':
    test()
