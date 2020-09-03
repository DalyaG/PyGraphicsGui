import json

from attr import dataclass


@dataclass
class BoundingBox:
    """
    Location of Waldo in *image pixels* coordinates
    """
    left: int
    top: int
    right: int
    bottom: int

    def to_list(self):
        return self.left, self.top, self.right, self.bottom

    def to_json(self, json_file_path: str):
        d = self.__dict__
        json.dump(d, open(json_file_path, 'w'), indent=4)

    @staticmethod
    def from_json(json_file_path: str):
        d = json.load(open(json_file_path, 'r'))
        return BoundingBox(**d)

    def contains(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom
