# Sage
A simple (absolutely simple) web-app for forecasting any univariate time series.
## Inspiration
**An hour of planning can save you ten hours of doing**

Planning is a very essential part of our lives. We spend a lot of time planning and rightly so because nothing gives more content than an efficient planning gone right. What can really help us achieve this is data driven planning. 

Having the opportunity to closely work with the management of a business, I came across innumerous situations when we wanted to plan ahead. One of the ways of doing this was to use our historical data to project the future trend of various aspects like monthly sales, inventory stock outs, customer traffic, manpower availability etc. 

With the advent of digital world, many small and large businesses have the data but do not have the technical know how of using this data for such type of forecasting. There is no universal solution which can be used to provide predicitions on various aspects in real time, and at the same time, be cost effective. 

## What it does
Sage is, as I call it, an absolutely simple web-app which can be used to forecast any univariate time series with a few clicks and within seconds! 
The app takes in historical data of the variable to be predicted and provides the option to either tune the forecasting model by itself or use your domain knowledge and do it on your own.
## How I built it
The forecasting model used in Sage is built using Facebook's Prophet. Prophet is a forecasting procedure implemented in Python. The first phase of the prototype was to try Prophet with a few datasets. The next step was to interface it with a UI. The UI of the web app is built on Dash - A Python web application framework written on top of Flask, Plotly.js, and React.js
## Challenges I ran into
The biggest challenge was to make the app easy to use. The forecasting model should be flexible and at the same time accurate. What really came handy in this was Prophet. Prophet provided accurate, fast and tunable forecasts.
Another challenge I faced was getting the UI up to the mark. Even though Dash has a detailed documentation, there were a few complications involved with the callback architecture of Dash.  

## Accomplishments that I'm proud of
This was the first time I was developing a project for a hackathon and that too all by my own. I am really happy I could do this. 
The forecasting done is of good accuracy and at the same time I was able to capture my objective of making the solution easy to use for even a non technical user. This was very fulfilling.
## What I learned
While developing this web-app, I got an opportunity to sharpen my python skills. It was also the first time I was working with an ML based library - fbprophet. I was able to learn other cool techs like Dash and plotly.
## What's next for Sage
I am very excited to have developed Sage upto this level and am looking forward to develop additional features in this to make it an even more exciting product. Next in my plan is:
* Integrate Sage with online univariate time series datasets to be able to use Sage out of the box. This can be useful for preforming forecasting on public available data.
* Provide capability to compare multiple forecasts. For eg. compare sales forecasts of item A and item B.
* Allow user specific profiles to save parameter preferences. 
* Better model diagnostic metrics to provide greater visibility into improving the model.

## Demo Link
https://youtu.be/3Uaebrb43Ww
