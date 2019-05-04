# Item Catalog
## Background
This is a project from the free Udacity course [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) and part of an old version of the Full Stack Web Developer Nanodegree.
## Description
This is an item calalog web application, where a user can view, create, edit and delete restaurants and menu items.
## Goals
* Develop a RESTful web application using the Python Flask framework.
* Use an ORM as an alternative to SQL.
* Implement CRUD operations.
* Add JSON endpoints to the application.
* Work with the iterative development process.
## Requirements
An installation of [Virtual Box](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html), and [Python](https://www.python.org/downloads/).
## Usage

* Clone or download this project (from the parent directoy) into your computer.
* Open your prefered terminal window and navigate to the folder with the files, enter the vagrant folder and run:
`vagrant up`
* When the console is ready, run `vagrant ssh`
* Change directory to /vagrant using: `cd /vagrant`
* Initialize database `python database_setup.py`
* Populate the database with sample data, running: `python lotsofmenus.py`
* Then run `http//:localhost:5000/restaurants` on your browser to test the item calalog web application.
