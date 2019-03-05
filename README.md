# Compound-Inventory-Search

Web-scraper and parser built with Python 2.7

The Advanced Clinical Chemistry Diagnostic Laboratory specializes in developing liquid chromatography mass spectrometry methods for the detection and quantification of small molecules in a variety of matrices. Early in method development, reference standards are selected and purchased from commercial sources. For clinical assays, internal standards are used as a measure of quality control. Laboratory staff is required to keep up with inventory of these standards and make necessary purchases. Through our purchasing portal, a product name, product ID, and price, are all required from any commercial source. We have a trusted source in which we routinely purchase our products from. However, given that we require several different compounds at a time and the product's prices can change, gathering the information from the website can become time consuming. 

This script takes a list of compounds, searches the site in the background, gathers the necessary information, places them into an Excel file, and returns a list of all compounds with zero results. 

# Downloads
PhantomJS is a headless web browser scriptable with JavaScript, but can be used by Python via selenium.

To install:
  Install NodeJS (https://nodejs.org/en/)  /b
  Using Node's package manager install phantomjs: npm -g install phantomjs-prebuilt
  Install selenium
