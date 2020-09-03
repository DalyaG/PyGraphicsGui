#!/usr/bin/env python3
import os
from optparse import OptionParser

from src.window_manager import WindowManager

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--image_path",
                      type="str",
                      default=None,
                      help="Input where-is-waldo image.")
    parser.add_option("-w", "--waldo_bounding_box_json_file_path",
                      type="str",
                      default=None,
                      help="Bounding box of where is waldo.")
    parser.add_option("-d", "--debug",
                      default=False,
                      action="store_true",
                      help="Use this flag if you wish to see debug logs.")
    params, _ = parser.parse_args()

    if params.image_path is None:
        params.image_path = os.path.join("data", "where_is_waldo.jpeg")
        params.waldo_bounding_box_json_file_path = os.path.join("data", "waldo_bounding_box.json")

    app = WindowManager(params.image_path, params.waldo_bounding_box_json_file_path, params.debug)
    app.run()
