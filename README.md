# ts-annotator

## What it is

Source code for [tabular data annotator](insert heroku link) webapp, built using [plotly dash](https://plotly.com/dash/). Originally it was intended for time series data, hence the repo's name.

## How it works

- Load data from a _csv_ (make sure csv is comma-separeted) or _xlsx_
- Select _x-axis_ (datetime or numeric dtype) and _y-axis_ (numeric dtype) to plot
- Input label value and select form color
- Draw rectangle or closed freeform in the graph to assign label
- Download results as _csv_ file

## Use it locally

To run the webapp locally using docker:
- clone the repo
- build the docker image
- run docker

```
git clone https://github.com/FBruzzesi/ts-annotator.git
docker build . -t ts-annotator
docker run -p 8080:8080 ts-annotator
```


## Issues

Issues and feedbacks are more than welcome

## Support
<a href='https://ko-fi.com/L3L37807E' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L37807E)
