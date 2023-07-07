<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

<h1 align=center>Individual Project Nº1</h1>

<p>The objetive of this project is to make an API for streaming movie platforms, and successfuly deploy it on the cloud, in this case <b>RENDER</b> cloud provider was used to deploy a api server and a postgres database.</p>

<p><b>Original CSV datasets source:</b>https://drive.google.com/drive/folders/1b49OVFJpjPPA1noRBBi1hSmMThXmNzxn?usp=drive_link</p>

<p>For cloud services cost reasons everything was put in a docker container, for anyone can easily run it in localhost with the followings commands</p>

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

<p>In this part the transformation and load was made as the following instructions indicate.</p>

* Generate 'id' attribute.
* Fill null values in ratings column with 'G'.
* Dates in format AAAA-mm-dd.
* Attributes containing text to lower case.
* Divide column duration.

<h2>API </h2>

<p>This part was made using the following frameworks and modules.</p>

* FastAPI
* PostgreSQL
* Pandas
* Pyarrow(parquet engine)
* Psycopg2

<p align=center><img src=img/newDocs.png><p>

<p>The api querys were made using <b>psycopg2</b> module to comunicate with a remote postgresql database where the datasets were allocated.</p>
<p>Function 2 endpoint was made using pandas  because ratings dataset CSV combined was too big to upload to the remote database and github, so it was transformed to parquet format, thereby a 385mb CSV file was transformed in a 29.5mb parquet file to work well with pandas instead of sql.</p>

<h2>DEPLOYMENT </h2>

<p>Deployment was made using <b>RENDER</b> and the following services.</p>

* Web Services: A free limited server, to build and deploy your sevices from github.
* PostgreSQL: A free limited remote database.

<p align=center><img src=img/renderDashboard.png><p>

<p>To use postgresql services you need to have it installed in your pc because the sending of CSVs is done by local server to remote server. PROBLEM: The rating csv was too big for the remote server so it is not in the database, the remaindings CSVs are in the remote db.</p>

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

<p align=center><img src=img/spacejungle.png><p>

<p align=center><img src=img/spacejungle-dt.png><p>

<p>With 'space jungle' it returns only 'tv show' types with the highest scores.</p>

<p align=center><img src=img/themanwhokillhitler.png><p>

<p align=center><img src=img/themanwhokillshitler-dt.png><p>

<p>Here it returns only 'movies' types with the highest scores.</p>



