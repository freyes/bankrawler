import sys
import codecs
import os.path
import base64
from scrapy.selector import XPathSelector
from scrapy.http import TextResponse
from BeautifulSoup import BeautifulSoup

def shell(use_plain=False, namespace=None):

    if namespace is None:
        namespace = {}

    try:
        if use_plain:
            # Don't bother loading IPython, because the user wants plain Python.
            raise ImportError
        try:
            from IPython.frontend.terminal.embed import TerminalInteractiveShell
            shell = TerminalInteractiveShell()
            shell.mainloop()
        except ImportError:
            # IPython < 0.11
            # Explicitly pass an empty list as arguments, because otherwise
            # IPython would use sys.argv from this script.
            try:
                from IPython.Shell import IPShell
                shell = IPShell(argv=[], user_ns=namespace)
                shell.mainloop()
            except ImportError:
                # IPython not found at all, raise ImportError
                raise
    except ImportError:
        import code
        # Set up a dictionary to serve as the environment for the shell, so
        # that tab completion works on objects that are imported at runtime.
        # See ticket 5082.
        imported_objects = {}
        try: # Try activating rlcompleter, because it's handy.
            import readline
        except ImportError:
            pass
        else:
            # We don't have to wrap the following import in a 'try', because
            # we already know 'readline' was imported successfully.
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(imported_objects).complete)
            readline.parse_and_bind("tab:complete")

        # We want to honor both $PYTHONSTARTUP and .pythonrc.py, so follow system
        # conventions and get $PYTHONSTARTUP first then import user.
        if not use_plain:
            pythonrc = os.environ.get("PYTHONSTARTUP")
            if pythonrc and os.path.isfile(pythonrc):
                try:
                    execfile(pythonrc)
                except NameError:
                    pass
            # This will import .pythonrc.py as a side-effect
            import user
        code.interact(local=namespace)


def main():
    fname = sys.argv[1]

    bank, asctime, url_base64 = fname.split("_")
    url_base64 = url_base64.replace(".html", "")
    url = base64.b64decode(url_base64)

    f = codecs.open(fname, "r")

    response = TextResponse(url_base64, body=f.read())
    xhs = XPathSelector(response)
    f.seek(0)
    dom = BeautifulSoup(f)
    f.seek(0)

    shell(namespace={"xhs": xhs,
                     "dom": dom,
                     "f": f})

    f.close()


if __name__ == '__main__':
    main()
