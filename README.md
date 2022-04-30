# HackUPC 
# Introduction
This is the repository of our Project for HackUPC 2022 called: HouSee

# About the project
We had used the restb.ai API to identify and quantificate different house features and characteristics.
To obtain the pictures and the data we have done web scrapping using requests and selenium on the fotocasa webside. 

# Usage of the App

The user provides the url of the house he or she wants to rate and then the app shows the pictures with the different characteristics, features and images stracted via the API and the webscraping. We also  provide the possibility to the user to do age recognition using the camera and comparing that age to an age we approximate the house will fit in (thank's to the information extracted previously). Thank's for this we can estimate if the house will match with the client. 

# Notes

The extraction of the age is based on the web <https://www.geeksforgeeks.org/age-detection-using-deep-learning-in-opencv/>, we use the pretrained model to identify the age of the user based on a picture.

# Authors

Pablo Vega Gallego pablo.vega.gallego@estudiantat.upc.edu

Lluis Pujalte Feliu De Cabrera llpfdc@gmail.com

