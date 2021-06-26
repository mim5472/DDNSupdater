# DDNSupdater
Check and update your Dynamic DNS IP address.

# How to use.
$ python3.7 ./dynamicdnsquery.py -h
usage: dynamicdnsquery.py [-h] fqdn nsserver

positional arguments:
  fqdn        Enter Fully Qualified Domain Name.
  nsserver    Enter a DNS server.

optional arguments:
  -h, --help  show this help message and exit

#Example.
$ python3.7 ./dynamicdnsquery.py your-DDNS-FQDN 8.8.8.8

#Check the log file for information/error message.
$ more ddnsquery.log