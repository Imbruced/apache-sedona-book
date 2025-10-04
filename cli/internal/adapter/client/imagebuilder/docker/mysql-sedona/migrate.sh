#!/bin/bash
# This script is used to migrate the MySQL database schema and data.

mysql -h localhost -u sedona -p sedona --password=sedona < /app/mysql_ddl.sql
