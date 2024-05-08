#!/bin/sh

echo $APP_PATH
path_project=$APP_PATH

echo 'export APP_PATH='$path_project >> ~/.bashrc
echo 'cd $APP_PATH' >> ~/.bashrc

# Enter the source directory to make sure the script runs where the user expects
cd $path_project

export APP_PATH=$path_project
if [ -z "$HOST" ]; then
		export HOST=0.0.0.0
fi

if [ -z "$PORT" ]; then
		export PORT=80
fi

export PATH="/opt/python/3.9.7/bin:${PATH}"
echo 'export VIRTUALENVIRONMENT_PATH='$path_project'antenv' >> ~/.bashrc
echo '. antenv/bin/activate' >> ~/.bashrc
PYTHON_VERSION=$(python -c "import sys; print(str(sys.version_info.major) + '.' + str(sys.version_info.minor))")
echo Using packages from virtual environment 'antenv' located at $path_project'/antenv'.
export PYTHONPATH=$PYTHONPATH:$path_project"/antenv/lib/python$PYTHON_VERSION/site-packages"
echo "Updated PYTHONPATH to '$PYTHONPATH'"
. antenv/bin/activate
nohup python $path_project/manage.py process_tasks &
# Running background-tasks
GUNICORN_CMD_ARGS="--timeout 600 --access-logfile '-' --error-logfile '-' -c /opt/startup/gunicorn.conf.py --chdir="$path_project gunicorn agritop_backend.wsgi


