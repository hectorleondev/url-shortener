# Url Shortener Api

This template includes samples how to install the application and documentation about the endpoints.

First of all I think that lambdas and API Gateway is the best approach because it is not part challenge that we need to handle horizontal scaling, minimum number of  active instances, for those requirement we need other solution like docker, ec2 instances.

Second I am using Serverless Framework because it is a easy way to interact with aws services and deploy my solution. 

Finally I decided to use a NoSQL solution like DynamoDB instead of Sequel database. Because
is an small project and there are not relations with other tables. If we want to add more complexity like user, roles probably we need to use a sequel database like Postgress or MySQL.

## Environment Information
Domain: https://5c4anzxltl.execute-api.us-east-1.amazonaws.com


## Install
```
Setup your amazon credential in your credentials file [official documentation](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/)

Run the following command

$ git clone https://github.com/hectorleondev/url-shortener.git
$ cd url-shortener
$ npm install
$ serverless deploy

Deploying calculator-api to stage dev (us-east-1)

✔ Service deployed to stack url-shortener-dev (170s)

```

## Endpoints

### Create new shortcode

```bash
curl --location 'https://5c4anzxltl.execute-api.us-east-1.amazonaws.com/dev/shortcode' \
--header 'Content-Type: application/json' \
--data '{
    "url": "<URL>",
    "title": "<TITLE>"
}'

response 
{
    "shortcode": "XXX1AA2"
}
'
```

_Note_: URL field is required but TITLE is optional


### Get URL data from shortcode
```bash
curl --location 'https://5c4anzxltl.execute-api.us-east-1.amazonaws.com/dev/url?shortcode=<SHORTCODE>'

response
{
    "url": "https://test.com/blog/test.html",
    "title": "Title link",
    "created_at": "2000-01-01 00:00:00"
}
```
_Note_: SHORTCODE param is required

### Get existing shortcode from url


```bash
curl --location 'https://5c4anzxltl.execute-api.us-east-1.amazonaws.com/dev/shortcode?url=<URL>'

Response
{
    "shortcode": "XXX1AA2"
}
```
_Note_: URL param is required.
Also I added that endpoint because if the user try to create new shortcode with a registered url.
I think that the solution must have other endpoint to handle that cases


## Unit test
```bash
Run the following command in root path
$ pip3 install -r requirements_test.txt
$ pytest tests --cov=src/

```


