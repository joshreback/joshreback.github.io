---
layout: post
title: How To Structure Code
---

Recently, I’ve been working on adding unit tests to an application I have been building over the past several months. There were several methods that conceptually were quite simple but turned out to be annoying and challenging to test. This felt wrong, so I decided to reflect on why and investigate how I could build simple-to-write and simple-to-test software — this post captures my learnings throughout this process.

——— 

### The Evolution of A Simple Method

There were a number of methods that were structured as follows:

V1
```python
def my_method(record_ids):
  """
  Return a DataFrame of records, grouped by an <id> field.
  
  Args:
    record_ids: a list of record_ids

  Returns:
    (Pandas.DataFrame) containing grouped records corresponding to ids.
  """

  # Create db connection
  # Fetch records from DB 
  # Convert into a DataFrame where each row represents a record: record_id | id | …other cols...
  # Group records by the <id> field and do some other preprocessing
  # Returned the grouped dataframe
```


I had thought of this as a simple, singular purpose function…given some ids, return a processed dataframe consisting of records corresponding to those ids. However, in between those inputs and outputs, I needed to call out to a database. In order to test this method, my naive first thought was to create a live database for this method to call out to. This, however, is obviously a bad practice when writing unit tests; unit tests should not connect to any external services. So the next thought was to patch the call to the database. At this point, patching is now generally regarded as a bad practice when writing tests. Why? Because patching requires understanding the guts of the method and necessitates careful surgery to ensure that the right class’s method are patched. It’s more an exercise in getting the test to pass than in verifying that the code works. Tests that use patching are also very tightly coupled to the implementation. 

My next thought, slightly better but still not great, was to pass in the database connection as a parameter to the method. Having the I/O in the guts of the method is what made it hard to test, so let’s pull it out and pass it in as a parameter. Now, the method-to-test had the following general structure: 

V2
```python
def my_method(record_ids, db_conn):
  """
  Return a DataFrame of records, grouped by an <id> field.
  
  Args:
    record_ids (List): a list of record_ids
    db_conn (SQLite.connection): A connection to the database.

  Returns:
    (Pandas.DataFrame) containing grouped records corresponding to ids.
  """

  # Fetch records from DB using db_conn
  # Convert into a DataFrame where each row represents a record: record_id | id | …other cols...
  # Group records by the <id> field and do some other preprocessing
  # Returned the grouped dataframe
```


Now, to test this method, we can use mocks instead of patches. In the test code, we create a mock object in place of an actual SQLite connection object, and tell it, “when your ‘execute’ method is called, return xyz objects instead of actually trying to execute a SQL query”. This technique of pulling out dependencies and passing them in as parameters is fittingly referred to as dependency injection. However, I still felt like this approach was lacking. I like to write lots of small, clear unit tests that test all kinds of combinations of inputs. However, I realized that with this approach, each unit test required two discrete steps. First, I had to create a mock object, and second, I had say what that mock object should return when its fetch method was called. The “various combinations of inputs" I’m interested in testing are captured by what the mock object returns (the second part of each test), so why am I wasting precious space in what should be small unit tests creating a mock object and mocking its return values? That exercise adds no useful information to my test - all it does is add mental overhead for whomever is trying to read and understand this test. 

The final iteration here was to make this method totally ignorant of any database at all. The behavior I’m interested in testing is that the original dataframe object gets transformed into a “grouped” dataframe object properly. So, I’ll pare the method back so that includes only that code:

V3
```python
def my_method(records_df):
  """
  Return a DataFrame of grouped records.
  
  Args:
    records_df (Pandas.DataFrame): a dataframe where each row consists of a reords

  Returns:
    (Pandas.DataFrame) containing grouped records corresponding to ids.
  """

  # Group records by the <id> field and do some other preprocessing
  # Returned the grouped dataframe
```

This is an easy method to test. It is also trivial to add tests that target different corner cases…All I have to do is construct an input dataframe of records. This requires no patched external services and no mock objects. And in reading the tests for this method, there is no mental overhead. All you need to keep track of, as the reader, is what data goes in and what data is returned. 

### The Big Ideas

This was originally an unguided process, but it turns out there are some big ideas about software development here. The essential idea has been called different things by different smart people - Functional Core / Imperative Shell by Gary Bernhardt, The Clean Architecture by Bob Martin (“Uncle Bob”) - but it generally centers around structuring code in the way outlined above. All of the I/O, or any code that must hold onto state, should be pushed to the periphery of your application. The “core” should consist of functional methods - functional meaning the method holds no state and therefore the only information you need to fully reason about the method’s behavior are its inputs and outputs. So in my example above, V3 of “my_method” is now a functional method - it takes a dataframe as input and returns a dataframe as output. There should be many of these types of methods at the core of the application with lots of accompanying unit tests. The calling code would be responsible for retrieving the records from the database and passing those records to “my_method”. 

Structuring your code in this way makes it very easy and natural to throw lots of unit tests at the functional methods in the core of the application. There should also be a few integration tests (which would likely use a live database for testing) to ensure that the parts all fit together properly, but not to test the business logic and corner cases.

A system constructed in this way is also very easily changeable, which is a first class concern in application development. Let’s say I need to switch from using a SQLite database to using a MySQL database. I would need to change my_method V1, as well as all other parts of my application where I connect to a database. If I don’t have a discipline of handling I/O at the periphery of my application, I’ll need to go track down all the places where I connect to SQLite, which will probably occur at different levels of abstraction. I’ll also likely need to update my tests unless there is some other indirection between my_method and the database connection object. Applications are generally not unique because of their database technology, or because of any technology choice for that matter, so changes to the database technology should not ripple throughout the entire codebase. Rather, applications are unique because of how they handle and process the data that is available to them. Therefore, applications should be structured and tested in a way that reflects the primacy of the logic around how data is handled rather than where it is stored.

### Final Thoughts

This was a very enriching learning experience because The Big Question here - how you should structure code - is more art than science. There is no one-size-fits-all approach, and the approach outlined above is not the best one for all types of software development, but it does make sense for many types of application development. Finally, it’s a question you will be forced to confront if you’re leading the development of a project that grows beyond a certain complexity threshold and into a “real" application. That’s when the pain of untestable code and inconsistent design patterns become most acute. To handle current and future complexity, you need to have some answer to the squishy question of how to structure code. 

If you want to learn more about these ideas, I recommend the following resources (all of which helped to shape my thinking):

- ![Functional Core Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) - the original screencast from Gary Bernhardt introducing the ideas behind the Functional Core Imperative Shell. Like all Destroy All Software content, it's short, dense (in a good way), and to the point.
- ![The Clean Architecture in Python](https://pyvideo.org/pyohio-2014/the-clean-architecture-in-python.html) - A very clear and comprehensive explanation of the Clean Architecture with Python code snippets. Also includes a lot of thoughtful discussion on implications for testing.
- ![The Grand Unified Theory of Software Architecture](https://danuker.go.ro/the-grand-unified-theory-of-software-architecture.html) - A very well-written and easy to follow explainer article on the Clean Architecture in Python video.