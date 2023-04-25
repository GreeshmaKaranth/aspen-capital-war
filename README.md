# Aspen Capital War

This is a repository for the Aspen Capital War take home project, which is a web application built with Python and MySQL. 
The project is designed to play the War game, as dictated by the rules given <a href="https://github.com/aspencapital/candidate-project-software-engineer">here</a>.

## Getting Started

To run the Aspen Capital War project locally, you'll need to follow these steps:

1. Install MySQL: <a href="https://dev.mysql.com/downloads/file/?id=518834">MySQL</a>
2. Open a terminal and run the following command to connect to MySQL and initialize database: 

<code> mysql -u <MYSQL_USER> -p 
       source initialize_db.sql
</code>

3. Install the required Python packages by running the following command:
<code>pip install -r requirements.txt</code>

4. Launch the flask app:
<code>flask --app aspen_capital_war run</code>

You can also use the Dockerfile to create Docker image and run the application

1. Build the docker image using the following commands:

<code>
- docker-compose build 
- docker-compose up 
</code>
<br>

2. Run the docker container:
<code> docker-compose run app </code>

## Reflection

I actually quite enjoyed this assignment. I liked exploring how to design this game, connect a backend MySQL server to it and create Flask endpoints for the same. I also enjoyed creating a complex docker file with these layered elements. 

If I have more time, I'd like to make the game a little more complex and verbose, adding interactive elements to it so that users can play the game themselves and see what scores they get with detailed explanations. I'd also explore making a cloud deployment, probably something that's a little more flexible and easy to adapt, by making use of Kubernetes and Helm charts.
