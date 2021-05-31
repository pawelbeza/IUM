# Machine Learning Engineering Course
## Task
> Predict purchase intention basing on logs from e-commerce shop

## Microservice

### Build Dockerfile
`docker build -t shopping-oracle -f ./microservice/Dockerfile ./microservice/`

### Run container
`docker run -d -p 8080:80 --name shopping_oracle shopping-oracle`
#### Quick note
Add volume `-v path_to_local_file_db:/app/app/predictions.db` if you want to persist your database on your host

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
    "click_rate" : 0,  
    "last_session_purchase" : true  
}  
EOF

#### Examplary output
{"model":"logistic_regression","prediction":true}

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
    "click_rate" : 0,  
    "last_session_purchase" : true  
}  
EOF  

#### Examplary output
{"model":"logistic_regression","prediction":true}

### Predictions archive
#### Run cmd line sqlite3 program
`docker exec -it shopping_oracle sqlite3 /app/app/predictions.db`
#### Query
sqlite> SELECT * FROM prediction;  
1|logistic_regression|102|0.0|553.0|1|1|0.0|1|4|4|0|0|0  
2|random_forest|102|0.0|553.0|1|1|0.0|1|4|4|0|0|1  
3|logistic_regression|102|0.0|553.0|1|1|0.0|1|4|4|0|0|0  
