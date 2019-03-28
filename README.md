# ECS781PMiniProject

RESTful application: ECS781P Cloud Computing Mini project

1. Dynamically generated REST API, API has set of services for the selected application domain, REST API responses conforming to REST standards (response codes)

2. The application makes use of an external REST service to complement its functionality: REST API for Twitter search https://api.twitter.com/1.1/search/tweets.json has been used.

3. The application uses a cloud database for accessing persistent information: kubernetes based load balancing, as well as Cassandra ring scaling

4. Database implementation including data schema design on Cassandra CQL, write operations involving INSERT statement

5. Documentation of the application code (in each of the code files, as well as in the README.MD file of the git repository).

5. Use of HTML web templates to display the results.


## Usage example

* Main page (/): The main page is defined in the HTML template user interface, it asks user to enter the query to search
* /database : The UI asks user to enter the query in the URL= database/{query} format
* /database/<query> : To search the results in the Cassandra database, User enters query in the form of database/{query}
* /database/search/ : Returns the JSON response list of all tweets in the stored database through GET request
* /tweetsearch : For the entered query on the main UI page, search in the stored Cassandra database first; if not found connect to Twitter external API



## Release History

* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`


## Contributing

1. Fork it (<https://github.com/SanketSadavarte/ECS781PMiniProject>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
