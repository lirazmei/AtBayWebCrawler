# AtBay Web Crawler System

Implementation of a web crawler system in python

* Ingest – The ingestion system must be able to receive multiple requests to initiate web
  page crawls in parallel under load. Per request, the system must acknowledge that the
  request has been received and provide the caller with a unique crawl-id assigned to
  each web page crawl.
* Process – The HTML of each web page should be extracted and stored in an accessible
  data store. The crawler system does not work under load but processes requests at its
  own pace individually (one by one).
* Status – an endpoint where a caller can check the status of a crawl using the unique
  crawl ID it received from the ingestion system.
  The available statuses are:

```
  Accepted – the request for a new crawl has been received and is pending processing
  Running – the crawl is currently running
  Error – an error occurred during the crawl (e.g. bad web page)
  Complete – the crawl was completed successfully
  Not-Found – the provided crawl-id could not be found
```

## System Requirements

* The crawl requests should indicate the targets in which to receive the notification. zero
  to multiple targets for a single crawl should be supported.

* If the status is completed we expect to get the location of the html file.
  Status checks should not create additional loads on any other system.
* Notifications – Once a crawl has been completed, the system should be able to notify
  the client through any of the following channels:

1. Email - Email address
2. Slack Message to User - User name
3. Slack Message to Channel - Channel Name

## Prerequisites

⁠ ⁠*Python* - This project based on Pyhton, current version is 3.9

* Design your solution as you would design for production purposes.
* Please use Python and specify the dependencies.
* You may use external tools.
* If you assume using an external system (DB, Cache, etc.), you may create a mock
  in code wrapping the calls to that system.
* The code could be provided within the GitHub repo, or a zip file, for your choice.

## Setup

* clone to the project

```bash
gh repo clone lirazmei/AtBayWebCrawler
```

* Create and activate Python virtualenv

```bash
cd /path/to/your/AtBayWebCrawler
virtualenv --python=python3.9 venv
source ./venv/bin/activate
```

* Install required modules in virtualenv

```bash
pip install -r requirements.txt
```

* Run the project

```bash
venv/bin/python app/main.py 
```

If you want to debug the project add "debug" arg to command line

```bash
venv/bin/python main.py debug
```

## HTTP Requests (GUI & curl )

To see the API that we have you can go to the following url:
<br>
http://127.0.0.1:8000/apidocs/
</br>

Or run the following curl requests in terminal:

1. curl -X POST "http://127.0.0.1:8000/crawl" -H "accept: application/json" -H "Content-Type: application/json" -d "
   "{\"url\": \"<<WANTED URL TO CRAWL>>\", \"communication_details\": { \"channel_name\": \"<relevant slack channel>\", \"email_address\": \"<relevant email>\", \"user_name\": \"<relevant username>\" }}
    2. For example:
       ``` curl -X POST "http://127.0.0.1:8000/crawl" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"communication_details\": { \"channel_name\": \"example_channel\", \"email_address\": \"example@gmail.com\", \"user_name\": \"example_name\" }, \"url\": \"https://ksp.co.il/web/\"}"```
2. curl -X GET "http://127.0.0.1:8000/crawl/<<crawl_id>>" -H "accept: application/json"
    3. For example:
       ``` curl -X GET "http://127.0.0.1:8000/crawl/4e078e11c2716b7e7720b718c42286d8" -H "accept: application/json" ```





