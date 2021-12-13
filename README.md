# ts-annotator

## What it is

Source code for [tabular data annotator](https://ts-annotator.herokuapp.com/) webapp hosted on [Heroku](https://www.heroku.com/), built using [plotly dash](https://plotly.com/dash/).

It was originally intended for time series data, hence the repo's name.

## Why it exists

Countless times a business expert or myself had to annotate tabular data, this solution made it faster.

## How it works

- Load data from a _csv_ (make sure csv is comma-separeted) or _xlsx_
- Select _x-axis_ (datetime or numeric dtype) and _y-axis_ (numeric dtype) to plot
- Input label value and select form color
- Draw rectangle or closed freeform in the graph to assign label
- Download results as _csv_ file

## Run locally
First step to run locally is to clone the repo:
```
git clone https://github.com/FBruzzesi/ts-annotator.git
```

### Using environment
Install _requirements.txt_ and then serve gunicorn server:
```
pip install -r requirements.txt
gunicorn --bind 127.0.0.1:8080 --pythonpath app index:server
```

### Using docker
To run the app using docker after cloning the repo, one should build the docker image and then run it:
```
docker build . -t ts-annotator
docker run -p 8080:8080 ts-annotator
```
Then go to http://localhost:8080/

## Issues

Issues and feedbacks are more than welcome

## Support

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L37807E)
