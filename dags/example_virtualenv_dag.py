import os

import pendulum

from airflow.decorators import dag, task


REQUIREMENTS_FILE = "requirements.txt"
PYTHON_VERSION = "3.9"


CUR_DIR = os.path.abspath(os.path.dirname(__file__))


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def example_with_virtualenv():
    def show_requirements():
        query = open(f"{CUR_DIR}/{REQUIREMENTS_FILE}", "r")
        req = query.readlines()

        query.close()

        return {"requirements": req}

    requirements = show_requirements()
    print("Requirements: ", requirements)

    @task.virtualenv(
        task_id="virtualenv_python",
        python_version=PYTHON_VERSION,
        requirements=requirements["requirements"],
        system_site_packages=True,
    )
    def callable_virtualenv():
        """
        Example function that will be performed in a virtual environment.

        Importing at the module level ensures that it will not attempt to import the
        library before it is installed.
        """
        from time import sleep

        from colorama import Back, Fore, Style

        print(Fore.RED + "some red text")
        print(Back.GREEN + "and with a green background")
        print(Style.DIM + "and in dim text")
        print(Style.RESET_ALL)
        for _ in range(4):
            print(Style.DIM + "Please wait...", flush=True)
            sleep(1)
        print("Finished")

    callable_virtualenv()


example_with_virtualenv()
