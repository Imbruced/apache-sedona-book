This chapter contains Apache Sedona application written in Python.

In the [sedona-initial-project](sedona-initial-project)
you can find a minimal Sedona application to get you started.

[simple-app.py](sedona-initial-project/src/simple-app.py)[app.py](sedona-initial-project/src/app.py) contains simple application
which starts a Sedona session, transforms WKT string inside the SQL query.

[app.py](sedona-initial-project/src/app.py) is more complex example
where we load data from CSV file, create spatial DataFrame and run spatial join based on the
ST_DWithin predicate. The goal of this example is to find number of restaurants 
for the atms within 500 meters distance.

In the [tests](sedona-initial-project/tests) you can find examples how to 
write tests for your Sedona applications using pytest framework.

To run the examples you need to make sure you have docker installed
on your machine and then you can run the following command from the

```bash
./submit_job.sh
```