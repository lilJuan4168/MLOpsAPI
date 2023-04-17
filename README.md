<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

<h1 align=center>Individual Project Nº1</h1>

<h3>ETL</h3>

<p>In this part transformation and load was made as the following instructions indicate.</p>

* Generate 'id' attribute.
* Fill null values in ratings column with 'G'.
* Dates in format AAAA-mm-dd.
* Attribures containing text to lower case.
* Divide column duration.

<h3>API </H3>

<p>This part was made using the followings frameworks and modules.</p>

* FastAPI
* PostgreSQL
* Pandas
* Pyarrow(parquet engine)
* Psycopg2

<p align=center><img src=img/apiEndpoints.png><p>

<p>The api querys were made using <b>psycopg2</b> module to comunicate with a remote postgresql database where the datasets were allocated.</p>
<p>Function 2 endpoint was made using pandas  because ratings datasets CSVs combined was too big to upload to the remote database and github, so it was transformed to parquet format, thereby a 385mb CSV file was transformed in a 29.5mb parquet file to work well with pandas instead of sql.</p>

<h3>DEPLOYMENT </h3>

<p>Deployment was made using <b>RENDER</b> and the following services.</p>

* Web Services: A free limited server, to build and deploy your sevices from github.
* PostgreSQL: A free limited remote database.

<p align=center><img src=img/renderDashboard.png><p>

<p>To use postgresql services you need to have it installed in your pc because the sending of CSVs is done by local server to remote server. PROBLEM: The rating csv was too big for the remote server so it is not in the database, the remaindings CSVs are in the remote db.</p>

<h3>EDA</h3>
<p>In this part exploratory analysis was made to decide what attribute is necessary for the ml model.</p>

<p align=center><img src=img/heatmap.png><p>

<p>Score and Type have been chosen for the ml model because its correlations are the lowest.</p>

<h3>ML</h3>
<p>The model Kmeans have been chosen for this recommender system, it is a cluster model to group attributes, label it and make prediction base on the labels.</p>

<p align=center><img src=img/clusterml.png><p>

<p>It is a simple 3 cluster Kmeans model, where one cluster group only the 'tv show' type instances, and the remainding two the 'movie' instances group by score, it works in the following manner.</p>

<ol>
<li>Get the score and type from the given movie title in get_recommendation() function.</li>
<li>model.predict([score, type]) --> label</li>
<li>Search and select the movies with the specific label ordered by score.
</li>
</ol>
