"""Monkey-patch .run(...)"""
import rethinkdb as r

from blab import app

original_run = r.ast.RqlQuery.run


def monkey_run(self, c=None, **kwargs):
    """Allows to .run() queries without explicitly passing a connection.

    :c: connection object
    :**kwargs: passes all args to original .run
    :returns: .run(...) result

    """
    if not c:
        with app.conn as c:
            return original_run(self, c, **kwargs)
    else:
        return original_run(self, c, **kwargs)

r.ast.RqlQuery.run = monkey_run
