import tkinter as tk

from src import logging_utils
import moderngl
from PIL import Image
from src.bounding_box import BoundingBox
from src.graphic_engine.graphic_engine import GraphicEngine
from src.graphic_engine.tkinter_framebuffer import TkinterFramebuffer
from tkinter import messagebox


class WindowManager:
    IMG_TAG = "IMG"
    FAIL_TAG = "FAIL"
    MAXIMAL_WINDOW_SIZE = [1600, 1200]
    WINDOW_TITLE = "Where Is Waldo"

    """
    Glossary:
    *********
    
    Graphic Concepts:
    -----------------

    context: Can be thought of as a "mediator" between python and the GPU, allows the creation of graphic abilities.
    
    graphic_engine: Handles the display of the image. 
                    Everything else is handled by the windows manager.
                    
    framebuffer: The "mediator" between the graphic engine and the Tkinter window.
                 In a simplified manner, one can imagine the following:
                 Tkinter knows how to display an image on a window (like a photo viewer),
                 but actually this image is constantly updating (because this how to computer screen works).
                 Which is like displaying a video that is composed of one repeating image.
                 So the framebuffer in some way "films" a video of the graphics generated by the graphic engine,
                 and turns it into a series of frames that can be displayed onto the Tkinter window.

    Window: The main window that shows the image.    
    
    Tkinter Concepts:
    -----------------

    root: Main Tkinter window.    
    main_canvas: Tkinter Canvas that occupies the entirety of the root window.
                 The main canvas both displays the graphics supplied by the graphic engine,
                 and is used as a, well, canvas, to draw GUI elements.
                                          
                                          
    Coordinates:
    ------------
    
    pixels coordinates: Type int, 0 <= x_pixels <= width, 0 <= y_pixels <= height.
                        The coordinates are [0,0] on the top left of the screen, and [width, height] on the bottom right.
                        Notice you have two different types of pixel coordinates - for the window and for the image.
    xy coordinates: Type float, -1 <= x <= 1, -1 <= y <= 1.
                    The coordinates are [-1, -1] on the bottom left of the screen, and [1, 1] on the top right.
                    This corresponds to the "window" coordinate system, where (0, 0) is the center.

    """
    def __init__(self, image_path: str, waldo_bounding_box_json_file_path: str, debug: bool = False):
        logging_utils.init_logger(log_level_for_console='debug' if debug is True else 'info')
        self._logger = logging_utils.get_logger()

        self.waldo_bounding_box = BoundingBox.from_json(waldo_bounding_box_json_file_path)
        self._fail_circle_radius = int(min([self.waldo_bounding_box.right - self.waldo_bounding_box.left,
                                            self.waldo_bounding_box.bottom - self.waldo_bounding_box.top]) / 2)

        image = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
        self._aspect_ratio = round(image.size[0] / image.size[1], 5)
        self.window_size: [int, int] = self._compute_initial_window_size(image.size)

        self.context: moderngl.Context = moderngl.create_standalone_context()
        self.graphic_engine = GraphicEngine(self.context, self.window_size, image)

        self.root = tk.Tk()
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(f'{self.window_size[0]}x{self.window_size[1]}')

        self.main_canvas: tk.Canvas = tk.Canvas(self.root)
        self.main_canvas.place(relwidth=1, relheight=1, anchor=tk.NW)

        self.framebuffer: TkinterFramebuffer = TkinterFramebuffer(self.context, self.window_size)
        self._add_framebuffer_image_to_canvas()

        self.root.protocol("WM_DELETE_WINDOW", self.before_closing)
        self.main_canvas.bind("<Configure>", self.on_resize)
        self.main_canvas.bind("<ButtonPress-1>", self.on_mouse_left_button_press)
        self.main_canvas.bind_all("<Key>", self.on_key_press)

        self._detections_circle_center_xy: [[float, float]] = []

    def run(self):
        self.root.mainloop()

    def before_closing(self):
        if messagebox.askokcancel("Quit", "Are you done looking for Waldo?"):
            self.on_closing()

    def on_closing(self):
        self.graphic_engine.destroy()
        self.root.destroy()

    def on_resize(self, tkinter_event: tk.Event):
        self._logger.debug(tkinter_event)
        self.window_size = [tkinter_event.width, tkinter_event.height]

        self.root.geometry(f'{self.window_size[0]}x{self.window_size[1]}')
        self.graphic_engine.on_resize(self.window_size)

        self._update_framebuffer_image()
        self._update_all_fail_circles()

    def on_key_press(self, tkinter_event: tk.Event):
        if tkinter_event.keysym == 'Escape':
            self.before_closing()

    def on_mouse_left_button_press(self, tkinter_event: tk.Event):
        self._logger.debug(tkinter_event)
        if self._is_this_waldo(tkinter_event.x, tkinter_event.y):
            self._successful_detection(tkinter_event.x, tkinter_event.y)
        else:
            current_detection_center_xy = self.graphic_engine.window_pixels_coordinates_to_xy_coordinates(tkinter_event.x,
                                                                                                          tkinter_event.y)
            self._detections_circle_center_xy += [current_detection_center_xy]
            self._draw_fail_circle(current_detection_center_xy)

    def _add_framebuffer_image_to_canvas(self):
        self.main_canvas.create_image(0, 0, image=self.framebuffer, anchor=tk.NW, tags=self.IMG_TAG)

    def _update_framebuffer_image(self):
        self.framebuffer = TkinterFramebuffer(self.context, self.window_size)
        self.main_canvas.delete(self.IMG_TAG)
        self._add_framebuffer_image_to_canvas()

        with self.framebuffer:
            self.graphic_engine.clear()
            self.graphic_engine.render()

    def _is_this_waldo(self, x_window_pixels: int, y_window_pixels: int) -> bool:
        xy_image_pixels = self.graphic_engine.window_pixel_coordinates_to_image_pixel_coordinates(x_window_pixels,
                                                                                                  y_window_pixels)
        return self.waldo_bounding_box.contains(*xy_image_pixels)

    def _successful_detection(self, x_pixels, y_pixels):
        r = self._fail_circle_radius * 2
        self.main_canvas.create_oval(x_pixels - r, y_pixels - r, x_pixels + r, y_pixels + r, outline='green', width=5.0)

        label = tk.Label(self.main_canvas, text="Well Done! You have found Waldo!",
                         font="Times 20 bold", borderwidth=2, relief=tk.GROOVE)

        button_ok = tk.Button(label, bg='pink', fg='black', font="Times 20 bold", relief=tk.RAISED,
                              text="Cool! Bye!", command=self.on_closing)
        button_ok.bind("<Enter>", lambda x: button_ok.config(background="magenta"))
        button_ok.bind("<Leave>", lambda x: button_ok.config(background="pink"))
        button_ok.pack(side='bottom', padx=5, pady=5, fill='x')

        self.main_canvas.create_window(*self._window_center, window=label, anchor=tk.CENTER,
                                       width=int(self.window_size[0]/2), height=int(self.window_size[1]/2))

    def _update_all_fail_circles(self):
        self.main_canvas.delete(self.FAIL_TAG)
        for detection_center_xy in self._detections_circle_center_xy:
            self._draw_fail_circle(detection_center_xy)

    def _draw_fail_circle(self, current_detection_center_xy: [float, float]):
        xy_pixels = self.graphic_engine.xy_coordinates_to_window_pixel_coordinates(*current_detection_center_xy)
        left, top = xy_pixels[0] - self._fail_circle_radius, xy_pixels[1] - self._fail_circle_radius
        right, bottom = xy_pixels[0] + self._fail_circle_radius, xy_pixels[1] + self._fail_circle_radius
        self.main_canvas.create_oval(left, top, right, bottom, outline='red', width=3.0, tags=self.FAIL_TAG)
        self.main_canvas.create_line(left, top, right, bottom, fill='red', width=3.0, tags=self.FAIL_TAG)
        self.main_canvas.create_line(left, bottom, right, top, fill='red', width=3.0, tags=self.FAIL_TAG)

    def _compute_initial_window_size(self, image_size: (int, int)) -> [int, int]:
        if image_size[0] <= self.MAXIMAL_WINDOW_SIZE[0] and image_size[1] <= self.MAXIMAL_WINDOW_SIZE[1]:
            return list(image_size)

        # For more info on this calculation, see https://stackoverflow.com/a/62307044/2934048
        image_to_window_ratio = ((image_size[0] / image_size[1])
                                 / (self.MAXIMAL_WINDOW_SIZE[0] / self.MAXIMAL_WINDOW_SIZE[1]))
        if image_to_window_ratio > 1:  # image is wider than window
            width = self.MAXIMAL_WINDOW_SIZE[0]
            height = int(self.MAXIMAL_WINDOW_SIZE[1] * (1 / image_to_window_ratio))
        else:  # window is wider than image
            width = int(self.MAXIMAL_WINDOW_SIZE[0] * image_to_window_ratio)
            height = self.MAXIMAL_WINDOW_SIZE[1]

        self._logger.debug(f"Image is larger than maximal window size, set initial window size to ({width}, {height})")

        return [width, height]

    @property
    def _window_center(self) -> [int, int]:
        return [int(self.window_size[0] / 2), int(self.window_size[1] / 2)]
