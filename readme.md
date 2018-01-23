User teaching status bot
========================

Shows if a person is currently teaching

Usage
------

`is Robert teaching` will see if Robert is in class


`when does Robert teach` will show you Robert's teaching schedule,
including when he teaches next.


parse aurora
------------

Open the page with the whole CS course listing in the course catelog. Save as courses.html,
run parseAurora.py, and pray.

This will output json to database.json. Restart statusbot.

Testing
-------

Too lazy to makefile this... run

    python -m unittest test
