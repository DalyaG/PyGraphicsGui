# PyGraphicsGui

A "[CookieCutter](https://github.com/cookiecutter/cookiecutter)" for a Pythonic GUI with custom graphics - 
clone this to jump-start your project and learn how to integrate between [ModernGL](https://github.com/ModernGL/ModernGL) 
and [Tkinter](https://docs.python.org/3/library/Tkinter.html) on Python3.6.

![Wondering what happens when tou find Waldo? You will have to find Waldo yourself!](../master/data/WhereIsWaldoDemo.gif)

Wondering what happens when you find Waldo? You will have to find Waldo yourself!

*This project has been tested on Windows10, Ubuntu18.04 and macOS Mojave.*


## Table of Contents


* [Starting Your Own Project](#starting-your-own-project)

* [PyGraphicsGui Capabilities](#pygraphicsgui-capabilities)

* [About This Project - The Technical Side](#about-this-project---the-technical-side)

    + [The Main Folder](#the-main-folder)
    
    + [The Source Folder](#the-source-folder)
    
    + [The Graphic Engine Folder](#the-graphic-engine-folder)

* [About This Project - My Personal Story](#about-this-project---my-personal-story)



## Starting Your Own Project

1. If you are on Ubuntu, [install Tkinter](https://stackoverflow.com/a/45442774/2934048) 
(on [Windows10](https://stackoverflow.com/a/53912930/2934048) and 
[macOS](https://www.python.org/download/mac/tcltk/) Tkinter is bundled with Python):

        sudo apt-get install python3.6-tk

1. Fork / Clone this repository

        git clone https://github.com/DalyaG/PyGraphicsGui.git

1. Install requirements:

        cd PyGraphicsGui
        
        pip3 install -r requirements.txt
        
1. Test your PyGraphicsGui app!
        
        python3 run_where_is_waldo.py
        
1. To integrate into your Pythonic pipeline:

        from src.window_manager import WindowManager
        
        app = WindowManager(image_path, bounding_box_json_file_path, debug)
        app.run() 


        
## PyGraphicsGui Capabilities

1. Click on the image with the left mouse button - if you didn't click on Waldo, 
you will see a red target and will be able to continue trying.

1. If you did click on Waldo - you will see a glorious exit message.

1. You can also press `esc` or the `x` on the top-right corner of the window (top-left on mac),
If you wish to close the app.

1. At any point, you can resize the window and the targets of the failed detections will stay where they should.


## About This Project - The Technical Side

This project was designed to be an as-lean-as-possible skeleton for a Pythonic desktop app with graphic capabilities.
At the same time, it is meant to be easily expanded upon, without thinking to much on technicalities such as 
"where should I put this?" or "How do I write tests?" etc.

To support the onboarding to this complex world, I have prepared an intro talk to computer graphics - 
the slides can be found here, video coming soon :)

In the meanwhile, I hope the many links below will help you develop your new skills :)

The structure of this project is as follows:

### The Main Folder

* This README

* Talk slides - with some more visual background on computer graphics and fun memes ;)

* Requirements file for easy install (on Ubuntu you also need to install Tkinter)

* `run_where_is_waldo` - a lean runner file to run this app from terminal.

* License - My goal in this project is to make this knowledge accessible, so you can do pretty much what you like
with the knowledge I gathered here. 

    If you publish something that is based on my work, be kind and link back to this project.

* `data` folder - contains the image to load and the location of Waldo (don't look!).

* `tests` folder - contains a base class that mocks the graphic engine, so that you could easily add tests to your app, 
and also an example tests file that validates some mathematical calculations.

### The Source Folder

As can be expected, the `src` folder is where the code is...

* `logging utils` holds a lean logger that helps with debugging, you can read more about it 
[here](https://codeburst.io/copy-pastable-logging-scheme-for-python-c17efcf9e6dc).

* `bounding box` is a lean dataclass that handles the location of Waldo

* `window_manager.py` is the main entry point - the class `WindowManager` creates and destroys the app,
handles user events, draws elements on screen, and communicates with the graphic engine. 

    To learn more about Tkinter you can browse [this](http://effbot.org/zone/tkinter-index.htm) website, 
    and I highly recommend the [sentdex Youtube channel](https://www.youtube.com/user/sentdex) - 
    most of what I know about Tkinter is from 
    [this](https://www.youtube.com/watch?v=HjNHATw6XgY&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk) tutorial.
    
### The Graphic Engine Folder 

I chose to put this in a separate folder (called `graphic_engine`, inside `src`) since once you start expanding on 
this project, and adding capabilities to your graphic engine, it helps to keep all the relevant logic in one place. 

For now this folder contains:

* `graphic_engine` holds the main entry point to all the graphic capabilities, which is now pretty lean.
The API is made up of mathematical conversion methods between the different coordinate systems. I included a 
glossary at the docstring of this class which I hope will take you the first steps in understanding this.

    I somehow managed to avoid the term "viewport" in my graphic engine implementation, but it's a useful one
    to know, as it appears *everywhere* in computer graphics. Learn more about viewport 
    [here](https://www.youtube.com/watch?v=DnEIdu8MpjY&list=PLE67F-VQUgLgws92d9gmP-AhBN_KQRGDW&index=18).
    
* `graphic_engine_initializer` is a helper that loads all the major graphics components, to avoid clutter in the
main graphic engine class. I plan to expand on this topic in the future, as this initializer holds the key to
understanding the basics of computer graphics, but for now we will settle for some external recommendations:

    * The first 3 minutes of 
    [this](https://www.youtube.com/watch?v=WMiggUPst-Q&list=PLRIWtICgwaX0u7Rf9zkZhLoLuZVfUksDP&index=2)
    video about vertex arrays (VAOs) and vertex buffers (VBOs) sorted out so many things in my head. 
    
    * The first half of [this](https://www.youtube.com/watch?v=21UsMuFTN0k) video helped me understand a bit 
    about framebuffers.
    
    * I learned a lot about graphics from 
    [this tutorial series](https://www.youtube.com/watch?v=dwt2NAd1ZYY&list=PL4neAtv21WOlqpDzGqbGM_WN2hc5ZaVv7)
    about [OpenFrameworks](https://openframeworks.cc/). 
    If you have some basic C++ knowledge I recommend you check it out.
    
    * [This](https://www.youtube.com/watch?v=-tonZsbHty8)
    is an excellent visual explanation about the model-view-projection matrix.
     
        And if you want to catch up on some linear algebra, it's always good (and fun!!) to watch some 
        3Blue1Brown videos, such as [this](https://www.youtube.com/watch?v=kYB8IZa5AuE).
    
    * [This](https://www.youtube.com/watch?v=vQ60rFwh2ig) is an excellent explanation about 
    [homogeneous coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates).
    
* `tkinter_framebuffer` is the "mediator" between the graphic engine and what is eventually presented on screen.
This implementation takes the rendered graphics and "projects" it onto an "image" that Tkinter recognizes. 
Tkinter "thinks" it's presenting an image when in fact it is presenting a projection of the graphics rendered
behind the scenes. 

    To understand how this object is initialized, you can read about Python's `with` statement
    [here](https://effbot.org/zone/python-with-statement.htm).

    Notice that this "image" has a constant size, and so this "mediator" needs to be re-initialized every time 
    the window size changes.  
    
    *A Thank You Note*: This object is almost a copy-paste of 
    [this framebuffer](https://github.com/moderngl/moderngl/blob/master/examples/tkinter_framebuffer.py) 
    from the moderngl repository. Understanding 
    [this](https://github.com/moderngl/moderngl/blob/master/examples/window_tkinter.py)
    example was a huge step for me. 
    
* `shaders` folder - a shader is a program that sends commands to the graphics card. It's basically a set of 
rules to apply to each pixel or object. 

    Although I am using the simplest shaders in this implementation, the first half of 
    [this](https://www.youtube.com/watch?v=C8FK9Xn1gUM&list=PLRIWtICgwaX0u7Rf9zkZhLoLuZVfUksDP&index=49)
    video really ties the room together.

    If you want to go a bit deeper - I learned a lot about shaders from 
    [this](https://www.udemy.com/share/102cOcAEEbeFZbRHsB/) course on Udemy. You can also find some free videos
    on [Youtube](https://www.youtube.com/watch?v=uwzEqeMd7uQ&list=PLFky-gauhF452rW98W4cyZ8_2fXBjfGOT).

## About This Project - My Personal Story

The first steps in computer graphics were the hardest I had to take. Not only is the math non-trivial, 
but also the available information online is not suitable for beginners - full of jargon and assumes advanced knowledge.

Add to that my vision to develop an interactive desktop app in Python, 
and you get a month full of blood, sweat, tears, and self doubt.

Once I was able to make my vision come to life, I knew I had to share my knowledge and make it accessible.

Since I made the first prototype, I am easily developing tools that help me in my job as a 
computer vision algorithms engineer. These tools assist me in making it as easy as possible for the human-in-the-loop
to participate in the AI flow.

My goal in this project is to make the onboarding stage of computer graphics as easy as possible, 
so that anyone could develop cool apps for fun and for work.

Hope you find this useful!
