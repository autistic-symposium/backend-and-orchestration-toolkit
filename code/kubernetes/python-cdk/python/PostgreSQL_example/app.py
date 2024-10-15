#!/usr/bin/env python3

from aws_cdk import core

from postgre_sql_example.postgre_sql_example_stack import PostgreSqlExampleStack


app = core.App()
PostgreSqlExampleStack(app, "postgre-sql-example")

app.synth()
