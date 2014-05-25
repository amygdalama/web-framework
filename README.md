A web framework written in Python, for week 1 of the [Iron Forger challenge](http://mathamy.com/introducing-iron-maker-or-forger-or-something.html).

# What it does
* Listens to HTTP Requests on a port of your choosing
* Parses URLs and attempts to route them to user-defined functions
* Looks files/directories to serve if a function doesn't exist for a URL
* If the URL corresponds to a directory, serves the `index.html` file in that directory (if it exists)
* Allows a user to have, uh, full access to your computer
