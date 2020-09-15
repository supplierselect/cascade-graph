# cascade-graph
Visualize ON DELETE cascade dependencies between SQL database tables - MySQL only for now

![Example graph](/deps.png)

## Install Requirements

 * Python 3.6
 * SQLAlchemy
 * Graphviz

## Use

casgraph.py is a command line script for generating Graphviz graphs of ON DELETE relationships 
between database tables. The output is saved as a PDF in the current working directory.

For help 

> ./casgraph.py -h

## Examples

To graph tables in the 'wives' database:
> ./casgraph -u henry -p theeighth wives 

Set credentials as environment variables:
>EXPORT MYSQL_USER=henry

>EXPORT MYSQL_PASSWORD=theeigth

To ignore 'repurcussions' table:
> ./casgraph --ignore repurcussions wives 

To show only cascade delete relationships:
> ./casgraph --rule CASCADE wives 

Use a different graphviz layout engine:
> ./casgraph --engine dot

## TODO

Contributions welcome:

 * Support for other databases
 * Output as other formats - e.g. SVG
