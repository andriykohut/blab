#!/usr/bin/env python3

import argparse

from rethinkdb.errors import RqlRuntimeError

from blab import app
from blab import config
from blab import loop


def runserver(host, port):
    if not app.r.db_list().contains(config.DB_NAME).run(app.conn):
        print("Database '{}' doesn't exist".format(config.DB_NAME))
        print("Try running 'initdb' command")
        return
    handler = app.make_handler()
    f = loop.create_server(handler, host, port)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()


def initdb():
    try:
        app.r.db_create(config.DB_NAME).run(app.conn)
        print("Database '{}' created successfully".format(config.DB_NAME))
    except RqlRuntimeError as e:
        print(e.message)


def main():
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest='cmd')
    runserver_cmd = subp.add_parser('runserver')
    runserver_cmd.add_argument('-H', '--host', dest='host',
                               default=config.APP_HOST)
    runserver_cmd.add_argument('-P', '--port', dest='port',
                               default=config.APP_PORT, type=int)
    subp.add_parser('initdb')
    args = parser.parse_args()
    if args.cmd == 'initdb':
        initdb()
    elif args.cmd == 'runserver':
        if not runserver(args.host, args.port):
            parser.exit(1)

if __name__ == "__main__":
    main()
