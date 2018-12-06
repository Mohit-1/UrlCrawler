# UrlCrawler

A RESTful API to test if the resource at a URL uses jQuery

### Installation instructions - 

1. Clone the repository

2. Install 'virtualenv' to create a virtual environment for our API

   `pip install virtualenv`

3. Setup the virtual environment

   `virtualenv sample_name_for_virtual_env`

4. Activate the virtual environment

   `sample_name_for_virtual_env\Scripts\activate`

5. Install the dependencies

   `pip install -r requirements.txt`

6. Set up the database (first change to the UrlCrawler directory)

   `python manage.py makemigrations`


   `python manage.py migrate`

7. Run the server (on localhost:8000)

   `python manage.py runserver`
   
### How it works -

The HTTP GET request contains a query parameter 'url'(with appropriate schema). The API consumes this request and uses the requests library, Beautiful Soup and re (Regular expressions module) to parse the HTML source of the resource to figure out if jQuery is being used.

### API reference - 

**End point** - /api/checkjquery?url=https://somerandomurl.com

**Methods allowed** - GET

**Optional Query params**

&verbose=yes - Queries the API for the first line in HTML source where jQuery reference was found

&getversion=yes - Queries the API for the version of jQuery being used in the HTML source       
