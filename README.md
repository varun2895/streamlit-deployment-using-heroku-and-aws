# streamlit-forecast-model

### ETL pipeline:

![image](https://user-images.githubusercontent.com/39857587/161380614-a2c3a669-9775-4ec6-8e36-5ccf698dae6c.png)


### Pushing data from S3 to Redshift table

    import psycopg2
    def redshift():
        conn = psycopg2.connect(dbname='dev', 
                                host='redshift-cluster-1.cdryosszv1il.ap-south-1.redshift.amazonaws.com', 
                                port='5439', 
                                user='awsuser', 
                                password='Password1')
        cur = conn.cursor();

        # Begin your transaction
        cur.execute("begin;")

        cur.execute("copy demandforecast from 's3://etllambdaredshift2/Forecast_data.csv' credentials 'aws_access_key_id=;aws_secret_access_key=' IGNOREHEADER 1 csv;")
        # Commit your transaction
        cur.execute("commit;")
        print("Copy executed fine!")
    redshift();


### Deployed on Heroku the Streamlit Application:

https://streamlit-forecast-model.herokuapp.com/
