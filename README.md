# show_int_tabular</b>
MDS show interface script that gives a tabular output of the show interface counters in the following categories:

show_int_tabular

positional arguments:
  fc_interface         fc interface, interface range or interface list. If not specified all FC interfaces are included.

optional arguments:
  -h, --help           show this help message and exit
  --version            version
  --statistics         Display statistics (non errors).
  --physical-errors    Display physical errors. Default
  --congestion-errors  Display congestion errors
  --e                  Display only (T)E ports in interface range or list
  --f                  Display only (T)F ports in interface range or list
  --np                 Display only (T)NP ports in interface range or list
  --edge               Display only logical-type edge ports in interface range or list
  --core               Display only logical-type core ports in interface range or list

