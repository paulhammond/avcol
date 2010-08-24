Avcol
=====

This is the image processing code behind http://favcol.com/, an unlikely attempt to find the favorite color of Flickr by analyzing photos that have been tagged "favcol". It uses cunning to overcome limitations in the App Engine Image Manipulation API - see http://www.paulhammond.org/2010/08/avcol/ for more details.

To get a dev environment set up:

1. Install the App Engine SDK, by following the instructions at 
http://code.google.com/appengine/docs/gettingstarted/devenvironment.html
3. Hope you don't have any weird conflicts between the App Engine SDK and the Python Imaging Library.
2. Run "dev_appserver.py /path/to/avcol"

To use it:

 . Visit /html?url=http://www.example.com/image.jpg for html output.
 . Visit /json?url=http://www.example.com/image.jpg for json output.

If you've made changes and you'd like to deploy them to Google's servers:

1. sign up at http://appengine.google.com/, click "create an application" and fill in the form.
2. edit the first line of app.yaml to use your application identifier.
3. run "appcfg.py update /path/to/avcol".

