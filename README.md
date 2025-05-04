
## Important

This tool does not have any security checks in place. Do not use it for live systems or in any environment outside of your development setup.


## AnyServer

This is a lightweight, simple, and dependency-free mockup RESTful API server that can be used right out of the box.
It is designed to assist developers in creating a RESTful frontend when the backend may not be available for testing or use.
One of the standout features of this server is its easy integration with mitmproxy, although this functionality will not be documented at this time. 
Any server is also useful for storing data collection gathered from various sources and can convert it into AXP. Can replicate certain functionalities without human intervention.




### Usage

The server is available in two versions: a single-file version (server.py) and the complete source code in the "include" directory. It is recommended to use the single-file version with command line options.

```
python3 anyserver.py --port 8999 --host localhost

```

```
python3 anyserver.py -h

```


### Data storage method
Any server offers two types of data storage: JSON files and GNUDB.
The JSON store saves data in small JSON files while keeping it in memory,
ensuring a fast response time for testing purposes.
On the other hand, GNUDB stores everything in its native format,
making it ideal for larger data collections. Additionally, SQLITE support will be added in the future

```
python3 anyserver.py --store_type dbm --port 8999 --host localhost

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


## FAQ

### Why Python? 

   I previously built several tools based on Node.js for this purpose,
 such as [statusBuffer](https://github.com/Soldy/statusBuffer), [predataBuffer](https://github.com/Soldy/preDataBuffer), and prodataBuffer.
 However, Node.js has changed significantly over time. Because of the lightweight nature of Node.js, the typescript, [the time](https://nodejs.org/en/blog/release) : code updates now take weeks to complete.
 Since the performance benefits of Node.js are no longer as pronounced, I've found rewriting in Python to be a more logical choice. 
 Python is preinstalled on most systems and offers various features that make it appealing for tool development,
 including support for writing [compressed files](https://docs.python.org/3.12/library/archiving.html), the [shelve](https://docs.python.org/3.12/library/shelve.html), [dbm](https://docs.python.org/3.12/library/dbm.html), and [SQLite](https://docs.python.org/3.12/library/sqlite3.html) ([I know I know](https://nodejs.org/docs/latest/api/sqlite.html)). Additionally, the MITM proxy is written in Python. For these reasons, creating a new tool in Python seems like a much more logical..



