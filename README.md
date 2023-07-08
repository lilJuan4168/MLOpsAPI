<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

<h1 align=center>MLOps IP Nº1</h1>

<h2>INTRO</h2>
<p>The objetive of this project is to make an API for streaming movie platforms, and successfuly deploy it on the cloud, in this case <b>RENDER</b> cloud provider was used to deploy a api server and a postgres database.</p>

<p><b>Original CSV datasets source:</b>https://drive.google.com/drive/folders/1b49OVFJpjPPA1noRBBi1hSmMThXmNzxn?usp=drive_link</p>

<p>For cloud services cost reasons database was put in a docker container, and the rest of the project can be easily executed with the followings commmands</p>


<h2>DEPLOYMENT</h2>
<pre>
#deploy postgresdb
docker compose up

#install dependencies
apt install -y postgresql-client
pip install -r requirements.txt

#create table in streaming database
./script.sh

#fill all tables with datasets
python3 datasets_loader.py

#start the API
uvicorn main:app --port 8000 --reload

#-----------------To close it ---------------------
docker compose down
</pre>



<h2>ETL</h2>

<p>In this part the transformation and load were made taking into account some indications from product owner and storage issues. The original datasets were .csv files, due to its big size, formats like .partquet compression were used to save storage and comply with github limits. All transformations are in ETL.ipynb file. List of ETL actions.</p>

* data type setting
* drop nulls
* data normalization
* split the datasets to fit the database design
* transform csv into parquet

<h2>DATABASE</h2>
<p>Postgresql was chose as database, it can be deployed in a docker container as indicated in 'Deployment part', it follows the following Entity relation diagram.</p>

<p align=center><img src=img/ERdiagram.png height=500 width=800><p>


<h2>API </h2>

<p>This part was made using the following frameworks and modules.</p>
<p>The api querys were made using <b>psycopg2</b> module to communicate with a remote postgresql database where the datasets were allocated.(first design with cloud database)</p>

* FastAPI
* PostgreSQL
* Pandas
* Psycopg2

<p align=center><img src=img/newDocs.png height=500 width=1000><p>


<h2>CLOUD HOSTING(first design deprecated) </h2>

<p>Deployment was made using <b>RENDER</b> and the following services.</p>

* Web Services: A free limited server, to build and deploy your sevices from github.
* PostgreSQL: A free limited remote database.

<p align=center><img src=img/renderDashboard.png height=400 width=1000><p>


<h2>EDA</h2>
<p>In this part exploratory analysis was made to decide what attribute is necessary for the ml model.</p>

<p align=center><img src=img/heatmap.png width=300 height=300><p>

<p>Score and Type have been chosen for the ml model because its correlations are the lowest.</p>

<h2>ML</h2>
<p>The model Kmeans have been chosen for this recommender system, it is a cluster model to group attributes, label it and make prediction base on the labels.</p>

<p align=center><img src=img/clusterml.png width=300 height=300><p>

<p>It is a simple 3 cluster Kmeans model, where one cluster group only the 'tv show' type instances, and the remainding two the 'movie' instances group by score, it works in the following manner.</p>

<ol>
<li>Get the score and type from the given movie title in get_recommendation() function.</li>
<li>model.predict([score, type]) --> label</li>
<li>Search and select the movies with the specific label ordered by score.
</li>
</ol>

<p align=center><img src=img/kmeansgraph.png><p>

<p>Kmeans graph of 3 clusters.</p>

<p>Example in use of the ML model.</p>

<p align=center><img src=img/spacejungle.png height=500 width=1000><p>

<p align=center><img src=img/spacejungle-dt.png height=400 width=1000><p>

<p>With 'space jungle' it returns only 'tv show' types with the highest scores.</p>

<p align=center><img src=img/themanwhokillhitler.png height=500 width=1000><p>

<p align=center><img src=img/themanwhokillshitler-dt.png height=400 width=1000><p>

<p>Here it returns only 'movies' types with the highest scores.</p>



