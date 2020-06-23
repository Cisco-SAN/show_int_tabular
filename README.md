
# show_int_tabular

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

**Sample Output:**


    MDS9000# python bootflash:show_int_tabular.py
    Link Stats:
    +---------------+--------------+-----------+-------------+---------------+-------------+--------+--------+--------+--------+--------+--------+---------------+-----------------+--------+--------+
    | Intf          | Link Failure | Sync Loss | Signal Loss | Invalid Words | Invalid CRC | NOS Rx | NOS Tx | OLS Rx | OLS Tx | LRR Rx | LRR Tx | FEC corrected | FEC uncorrected | BB_SCs | BB_SCr |
    +---------------+--------------+-----------+-------------+---------------+-------------+--------+--------+--------+--------+--------+--------+---------------+-----------------+--------+--------+
    | fc1/1         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/2         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/3         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/4         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/5         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/6         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/7         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/8         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/9         | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |
    | fc1/10        | 0            | 0         | 0           | 0             | 0           | 0      | 0      | 0      | 0      | 0      | 0      | 0             | 0               | 0      | 0      |

