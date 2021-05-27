# Machine Learning Engineering Course
## Task
> Predict purchase intention basing on logs from e-commerce shop

## Microservice

### Build Dockerfile
`docker build -t shopping-oracle -f ./microservice/Dockerfile ./microservice/`

### Run container
`docker run -d -p 8080:80 shopping-oracle`

### Run logistic regression prediction
#### Examplary request
curl --request POST http://localhost:8080/predict/logistic_regression \  
--header "Content-Type: application/json" \  
--data  @- << EOF  
{  
    "user_id": 102,  
    "offered_discount" : 0,  
    "price" : 553,  
    "duration" : 0.0,  
    "weekend" : false,  
    "weekday" : 4,  
    "hour" : 4,  
    "unique_item_views" : 1,  
    "item_views" : 1,  
    "click_rate" : 0,  
    "last_session_purchase" : true  
}  
EOF

#### Examplary output
{"model":"logistic_regression","prediction":false}

### Run random forest prediction
#### Examplary request
curl --request POST http://localhost:8080/predict/random_forest \  
--header "Content-Type: application/json" \  
--data  @- << 'EOF'  
{  
    "user_id": 102,  
    "offered_discount" : 0,  
    "price" : 553,  
    "duration" : 0.0,  
    "weekend" : false,  
    "weekday" : 4,  
    "hour" : 4,  
    "unique_item_views" : 1,  
    "item_views" : 1,  
    "click_rate" : 0,  
    "last_session_purchase" : true  
}  
EOF
#### Examplary output
{"model":"random_forest","prediction":true}

### Run AB prediction
It will predict purchase intention using one of above models. Choice of model will depend on the value of *user_id*
#### Examplary request
curl --request POST http://localhost:8080/predict/testAB \  
--header "Content-Type: application/json" \  
--data  @- << EOF  
{  
    "user_id": 102,  
    "offered_discount" : 0,  
    "price" : 553,  
    "duration" : 0.0,  
    "weekend" : false,  
    "weekday" : 4,  
    "hour" : 4,  
    "unique_item_views" : 1,  
    "item_views" : 1,  
    "click_rate" : 0,  
    "last_session_purchase" : true  
}  
EOF  

#### Examplary output
{"model":"logistic_regression","prediction":false}
