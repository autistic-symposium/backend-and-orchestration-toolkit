## airflow and luigi

<br>

### airflow

<br>

* **[apache airflow](https://github.com/apache/airflow)** was a tool **[developed by airbnb in 2014 and later open-sourced](https://medium.com/airbnb-engineering/airflow-a-workflow-management-platform-46318b977fd8)**

* it is a platform to programmatically author, schedule, and monitor workflows. when workflows are defined as code, they become more maintainable, versionable, testable, and collaborative

* you can use airflow to author workflows as directed acyclic graphs (DAGs) of tasks: the airflow scheduler executes your tasks on an array of workers while following the specified dependencies.

* here is **[a very simple toy example of an airflow job](https://gist.github.com/robert8138/c6e492d00cd7b7e7626670ba2ed32e6a)** that simply prints the date in bash every day after waiting for one second to pass, after the execution date is reached:

<br>

```python

from datetime import datetime, timedelta
from airflow.models import DAG  # Import the DAG class
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import TimeDeltaSensor

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 8),
}

dag = DAG(
    dag_id='anatomy_of_a_dag',
    description="This describes my DAG",
    default_args=default_args,
    schedule_interval=timedelta(days=1))   # This is a daily DAG.

# t0 and t1 are examples of tasks created by instantiating operators
t0 = TimeDeltaSensor(
    task_id='wait_a_second',
    delta=timedelta(seconds=1),
    dag=dag)

t1 = BashOperator(
    task_id='print_date_in_bash',
    bash_command='date',
    dag=dag)

t1.set_upstream(t0)
```

<br>

---

### luigi

<br>

- **[luigi data pipelining](https://github.com/spotify/luigi)** is spotify's python module that helps you build complex pipelines of batch jobs. it handles dependency resolution, workflow management, visualization, etc. 

- the basic units of Luigi are task classes that model an atomic ETL operation, in three parts: a requirements part that includes pointers to other tasks that need to run before this task, the data transformation step, and the output. All tasks can be feed into a final table (e.g. on Redshift) into one file.

- here is **[an example of a simple workflow in luigi](https://towardsdatascience.com/data-pipelines-luigi-airflow-everything-you-need-to-know-18dc741449b7)**:

<br>

```python
import luigi

class WritePipelineTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget("data/output_one.txt")

    def run(self):
        with self.output().open("w") as output_file:
            output_file.write("pipeline")


class AddMyTask(luigi.Task):

    def output(self):
        return luigi.LocalTarget("data/output_two.txt")

    def requires(self):
        return WritePipelineTask()

    def run(self):
        with self.input().open("r") as input_file:
            line = input_file.read()

        with self.output().open("w") as output_file:
            decorated_line = "My "+line
            output_file.write(decorated_line)
```

<br>

----

### airflow vs. luigi

<br>

|                                       |        airflow        |           luigi        |
|---------------------------------------|-----------------------|------------------------|
| web dashboard                            | very nice             |  minimal               |
| Built-in scheduler                    | yes                   |    no                  |
| Separates output data and task state  | yes                   |    no                  |
| calendar scheduling                   | yes                   | no, use cron           |
| parallelism                           | yes, workers          | threads per workers    |
| finds new deployed tasks              | yes                   | no                     |
| persists state                        | yes, to db            | sort of                |
| sync tasks to workers                    | yes                   | no                     |
| scheduling                            | yes                   | no                     |


<br>

---

### cool resources

<br>

* **[incubator airflow data pipelining](https://github.com/apache/incubator-airflow)**
* **[awesome airflow Resources](https://github.com/jghoman/awesome-apache-airflow)**
* **[airflow in kubernetes](https://github.com/rolanddb/airflow-on-kubernetes)**
* **[astronomer: airflow as a service](https://github.com/astronomer/astronomer)**
