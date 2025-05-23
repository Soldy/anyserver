
## Important

This tool does not have any security checks in place. Do not use it for live systems or in any environment outside of your development setup.


## AnyServer

  This is a lightweight, simple, and dependency-free mockup RESTful API server that can be used right out of the box.
It is designed to assist developers in creating a RESTful frontend when the backend is unavailable for testing or use.
One of the standout features of this server is its easy integration with mitmproxy, although this functionality will not be documented at this time.
  Additionally, anyserver is good for storing data collected from various sources and can convert it into AXP.
It is capable of replicating certain functionalities without human intervention.
  The search function is implemented.
However, please note that it may not perform well with large datasets.
Searching in small test data collections of 2-3 megabytes will work fine, but handling 2-gigabyte datasets will take a huge amount of time.


### Install

```
pip3 install restfullmonkey
```


### Usage

The server is available in two versions: a single-file version (server.py) and the complete source code in the "include" directory. It is recommended to use the single-file version with command line options.

```
python3 -m restfullmonkey --port 8999 --host localhost

```

```
python3 -m restfullmonkey -h

```


### Data storage method
Any server offers two types of data storage: JSON files and GNUDB.
The JSON store saves data in small JSON files while keeping it in memory,
ensuring a fast response time for testing purposes.
On the other hand, GNUDB stores everything in its native format,
making it ideal for larger data collections. Additionally, SQLITE support will be added in the future


#### dbm support
```
python3 restfullmonkey --store_type dbm --port 8999 --host localhost

```

### Please remember
This tool is intended for local use only. It has not undergone third-party security audits and should not be used in a live environment.

## Alternatives 


 + [Apidog - https://apidog.com/](https://apidog.com/)
 + [HoverFly - https://hoverfly.io/](https://hoverfly.io/)
 + [ApiGee - https://cloud.google.com/apigee](https://cloud.google.com/apigee)
 + [Postman - https://www.postman.com/](https://www.postman.com/)
 + [Mock Api - https://mocki.io/](https://mocki.io/)
 + [StopLight - https://stoplight.io/](https://stoplight.io/)
 + [Beexeptor https://beeceptor.com/mock-api/](https://beeceptor.com/mock-api/)
 + [jsonplaceholder - https://jsonplaceholder.typicode.com/](https://jsonplaceholder.typicode.com/)
 + [WireMock - https://wiremock.org/](https://wiremock.org/)

### Future

The project began as a simple hobby that I expected to take only two or three days. However, I quickly realized this tool was much more useful than I thought.
Most of the data my system collects is unorganized, so consolidating all this information into a single, burnable, and portable format offers numerous benefits.
I have already implemented support for DBM to handle more data, and I currently store 30 gigabytes of data in this way. Additionally, I plan to add data hashing soon. 
The next step will involve ensuring that SQLite supports. 256 TB limit is a significant amount of data storage. 
I also aim to develop a method for converting data from one type of storage to another. Looking ahead, I will be removing single-file support in the next release, as it will be replaced by a different solution.

## FAQ

### Why Python? 

   I previously built several tools based on Node.js for this purpose,
 such as [statusBuffer](https://github.com/Soldy/statusBuffer), [predataBuffer](https://github.com/Soldy/preDataBuffer), and prodataBuffer.
 However, Node.js has changed significantly over time. Because of the lightweight nature of Node.js, the typescript, [the time](https://nodejs.org/en/blog/release) : code updates now take weeks to complete.
 Since the performance benefits of Node.js are no longer as pronounced, I've found rewriting in Python to be a more logical choice. 
 Python is preinstalled on most systems and offers various features that make it appealing for tool development,
 including support for writing [compressed files](https://docs.python.org/3.12/library/archiving.html), the [shelve](https://docs.python.org/3.12/library/shelve.html), [dbm](https://docs.python.org/3.12/library/dbm.html), and [SQLite](https://docs.python.org/3.12/library/sqlite3.html) ([I know I know](https://nodejs.org/docs/latest/api/sqlite.html)). Additionally, the MITM proxy is written in Python. For these reasons, creating a new tool in Python seems like a much more logical..



