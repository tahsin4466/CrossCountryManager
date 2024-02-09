# CrossCountryManager

## Overview
This is a web application built as a cross country data management system. It allows the user (admin) to handle and manipulate race data, see analytics, aggregate results and integrate a seperate IoT solution (remote camera) that can identify runner records based on images captured at the finished line. It includes advanced features, such as chart visualizations, a full MySQL database, user-facing management UI, automatic data collection and sorting as well as facial identification.

This project was built using a Flask backend and an HTML/CSS/JS front-end with Bootstrap 4 and jQuery. It also uses OpenCV facial recognition and MySQL using phpMyAdmin. It was built for a school event, the 2021 Cross Country (Hence its namesake). It has not been updated since, and is only here for archiving.

## Installation
PLEASE READ: This project relied on database infrastructure that is no longer available! It was run using a phpMyAdmin server, but that has since ceased to exist. You can attempt to run your own phpMyAdmin server, but it will not work otherwise. If you wish to continue, the rest of the steps are here:
Make sure you have the latest version of Python installed (preferabbly 3.12+).

This project requires Flask: a back-end framework for creating web applications. Using pip, run:

```
pip install flask
```

Make sure to have Flask configured to:
 - Target the file `app.py`
 - Media/static folder set to `static`
 - Templates folder set to `templates`

Numpy is also required for data analysis. Using pip, run:

```
pip install numpy
```

Next, we will need the requesite libraries for OpenCV image recognition. Install the following libraries in order:
```
pip install cmake
```
```
pip install opencv-python
```
```
pip install face_recognition
```

We will also need PyMySQL to interact with phpMyAdmin. To do so, install using pip:
```
pip install PyMySQL
```

Finally, we will need pygame to dynamically play sound effects and load video content. To do so, install using:
```
pip install pygame
```
   
Then, download this repository. Run `app.py`. You will see a localhost IP pop up in the terminal. Press the link to open the application in your browser. Again though, this will not work without a proper phpMyAdmin server of your own.

NOTE: This is an archive of a project completed in 2021. It is no longer maintained.


