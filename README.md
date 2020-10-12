
# show_int_tabular

MDS show interface script that gives a tabular output of the show interface counters in the following categories:

show_int_tabular version v1.8

positional arguments:

  fc_interface          fc interface, port-channel interface, interface range or interface list

optional arguments:

  -h, --help            show this help message and exit  
  
  --version             version
  
  --general-stats       Display general statistics (non errors)
  
  --link-stats          Display physical link statistics. Default
  
  --congestion-stats    Display congestion statistics
  
  --transceiver-stats   Display transceiver(SFP) statistics
  
  --sfp-stats           Display transceiver(SFP) statistics
  
  --transceiver-detail-stats
  
                        Display transceiver(SFP) detailed statistics
                        
  --sfp-detail-stats    Display transceiver(SFP) detailed statistics
  
  --e                   Display only (T)E ports in interface range or list
  
  --f                   Display only (T)F ports in interface range or list
  
  --np                  Display only (T)NP ports in interface range or list
  
  --edge                Display only logical-type edge ports in interface range or list
  
  --core                Display only logical-type core ports in interface range or list
  
  --errorsonly          Display only interfaces with non-zero counts.
  
  --outfile OUTFILE     Write output to file on bootflash on switch. If file exists already it will be overwritten.
  
  --appendfile APPENDFILE
  
                        Append output to file on bootflash on switch. If file does not exist it will be created.


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

