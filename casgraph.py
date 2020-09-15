#!/usr/bin/env python
import os
import sys
import argparse
from typing import Set

import graphviz
from sqlalchemy import create_engine
from sqlalchemy import engine

help_txt = '''
Generate Graphviz PDF of cascade dependencies between MySQL tables. MySQL username and
password can be set with command line arguments or as environment variables MYSQL_USER and
MYSQL_PASSWORD.
'''

parser = argparse.ArgumentParser(
    prog="Cascade Graph",
    description=help_txt,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
rule_help = "ON DELETE rules to consider - CASCADE, SET NULL, RESTRICT or all"

parser.add_argument(
    "-i", "--ignore", default="", help="tables to ignore, comma separated"
)
parser.add_argument("-r", "--rule", default="all", help=rule_help)
parser.add_argument("database", help="name of the database")
parser.add_argument("-u", "--user", help="MySQL username")
parser.add_argument("-H", "--host", default="localhost", help="Database hostname")
parser.add_argument("-p", "--password", default='', help="MySQL password")
parser.add_argument("-e", "--engine", default='fdp', help="Graphviz engine- e.g dot, neato")


def query(conn_string):
    eng = create_engine(conn_string)
    conn = eng.connect()
    q = f"""
    SELECT table_name, delete_rule, referenced_table_name
    FROM information_schema.REFERENTIAL_CONSTRAINTS
    WHERE constraint_schema = '{conn.engine.url.database}'"""
    return conn.execute(q)


def graph(relations_list, ignore_set: Set, rule="all", graph_engine='fdp'):
    g = graphviz.Digraph("G", filename="deps.gv", engine=graph_engine)
    for rel in relations_list:
        if ignore_set.intersection(set(rel)):
            continue
        if rule == "all":
            g.edge(rel.referenced_table_name, rel.table_name, label=rel.delete_rule)
        elif rel.delete_rule != rule:
            continue
        g.edge(rel.referenced_table_name, rel.table_name)
    return g


if __name__ == "__main__":
    args = parser.parse_args()

    if 'MYSQL_USER' in os.environ:
        user = os.environ['MYSQL_USER']
    else:
        user = args.user
        if not user:
            print('-u, --user or ENV variable MYSQL_USER must be set')
            sys.exit()
    if 'MYSQL_PASSWORD' in os.environ:
        pword = os.environ['MYSQL_PASSWORD']
    else:
        pword = args.password

    conn_string = f"mysql://{user}:{pword}@{args.host}/{args.database}"
    rel_list = query(conn_string).fetchall()
    i: str
    ignore_set = {i.strip() for i in args.ignore.split(",")}
    g = graph(rel_list, ignore_set, rule=args.rule, graph_engine=args.engine)
    g.view()
