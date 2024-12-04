// Import the express module
const express = require('express');

// Import the mysql module
const mysql = require('mysql');

// Create an instance of express
const app = express();

// Define the port number for the server to listen on
const port = 3000;

// Define the configuration for the MySQL database connection
const connectionConfig = {
    host: 'localhost', // Database host
    user: 'root', // Database user
    password: 'password', // Database password
    database: 'khmerpenalcode' // Database name
};

// Create a connection pool to manage multiple database connections
let pool = mysql.createPool(connectionConfig);

// Allow the application to parse JSON data in request bodies
app.use(express.json());

// Start the server and listen on the defined port
app.listen(port, function (err) {
    if (err) {
        // Log an error message if the server fails to start
        console.log("Error in server setup");
    } else {
        // Log a success message if the server starts successfully
        console.log(`Server running on port`, port);
    }
});

// Define a GET endpoint to retrieve all crimes from the database
app.get('/GetCrimes', (req, res) => {
    // Get a connection from the pool
    pool.getConnection(function (err, connection) {
        if (err) {
            // Log an error message if there is an error getting a connection
            console.log("Error: " + err);
            connection.release(); // Release the connection back to the pool
            return res.status(500).send(err); // Send a 500 Internal Server Error response
        }

        // Define the SQL query to select all crimes
        let sql = 'SELECT * FROM crime';

        // Execute the SQL query
        connection.query(sql, function (err, results) {
            if (err) {
                // Log an error message if there is an error executing the query
                console.log("Error: " + err);
                connection.release(); // Release the connection back to the pool
                return res.status(500).send(err); // Send a 500 Internal Server Error response
            }
            if (results.length == 0) {
                // If no results are found, send a 404 Not Found response
                connection.release(); // Release the connection back to the pool
                return res.status(404).send("Crimes not found");
            }
            // Send the results as a JSON response with a 200 OK status
            res.status(200).json(results);
            connection.release(); // Release the connection back to the pool
        });
    });
});

// Define a GET endpoint to retrieve a specific crime by ID from the database
app.get('/GetCrime', (req, res) => {
    // Check if the ID query parameter is provided
    if (req.query.ID == null || isNaN(req.query.ID)) {
        return res.status(400).send("ID is required"); // Send a 400 Bad Request response if ID is missing
    }
    // Get a connection from the pool
    pool.getConnection(function (err, connection) {
        if (err) {
            // Log an error message if there is an error getting a connection
            console.log("Error: " + err);
            connection.release(); // Release the connection back to the pool
            return res.status(500).send(err); // Send a 500 Internal Server Error response
        }

        // Define the SQL query to select a crime by ID
        let sql = `SELECT * FROM crime WHERE ID = ${req.query.ID}`;

        // Execute the SQL query
        connection.query(sql, function (err, results) {
            if (err) {
                // Log an error message if there is an error executing the query
                console.log("Error: " + err);
                connection.release(); // Release the connection back to the pool
                return res.status(500).send(err); // Send a 500 Internal Server Error response
            }
            if (results.length == 0) {
                // If no results are found, send a 404 Not Found response
                connection.release(); // Release the connection back to the pool
                return res.status(404).send("Crimes not found");
            }
            // Send the first result as a JSON response with a 200 OK status
            res.status(200).json(results[0]);
            connection.release(); // Release the connection back to the pool
        });
    });
});

// Define a GET endpoint to retrieve aggrivations and clauses for a specific crime by ID
app.get('/GetAggrivationAndClausesFromCrime', (req, res) => {
    // Get the ID query parameter
    var ID = req.query.ID;
    if (ID == null || isNaN(ID)) {
        return res.status(400).send("Crime ID is required"); // Send a 400 Bad Request response if ID is missing
    }

    // Get a connection from the pool
    pool.getConnection(function (err, connection) {
        if (err) {
            // Log an error message if there is an error getting a connection
            console.log("Error: " + err);
            connection.release(); // Release the connection back to the pool
            return res.status(500); // Send a 500 Internal Server Error response
        }
        // Define the SQL query to select aggrivations and clauses for a specific crime
        let sql = `SELECT * FROM aggrivations INNER JOIN clauses ON aggrivations.ClauseID = clauses.ClauseId WHERE CrimeID = ${ID}`;

        // Execute the SQL query
        connection.query(sql, (err, results) => {
            if (err) {
                // Log an error message if there is an error executing the query
                console.log("Error: " + err);
                connection.release(); // Release the connection back to the pool
                return res.status(500).send(err); // Send a 500 Internal Server Error response
            }
            if (results.length == 0) {
                // If no results are found, send a 404 Not Found response
                connection.release(); // Release the connection back to the pool
                return res.status(404).send("Aggrivations not found");
            }
            // Send the results as a JSON response with a 200 OK status
            res.status(200).json(results);
            connection.release(); // Release the connection back to the pool
        });
    });
});

// Define a GET endpoint to retrieve an article and its clauses by article number
app.get('/GetArticleAndClauses', (req, res) => {
    // Get the Article query parameter
    var ID = req.query.Article;
    if (ID == null || isNaN(ID)) {
        return res.status(400).send("Article is required"); // Send a 400 Bad Request response if Article is missing
    }

    // Get a connection from the pool
    pool.getConnection(function (err, connection) {
        if (err) {
            // Log an error message if there is an error getting a connection
            console.log("Error: " + err);
            connection.release(); // Release the connection back to the pool
            return res.status(500); // Send a 500 Internal Server Error response
        }

        // Define the SQL query to select an article and its clauses
        let sql = `SELECT *, (SELECT JSON_ARRAYAGG(JSON_OBJECT('English',clauses.ClauseEnglish,'Khmer',clauses.ClauseKhmer,'ID',clauses.ClauseId)) FROM clauses WHERE clauses.ArticleNumber = articles.ArticleNumber) AS clauses FROM articles WHERE articles.ArticleNumber = ${ID}`;

        // Execute the SQL query
        connection.query(sql, (err, results) => {
            if (err) {
                // Log an error message if there is an error executing the query
                console.log("Error: " + err);
                connection.release(); // Release the connection back to the pool
                return res.status(500).send(err); // Send a 500 Internal Server Error response
            }
            if (results.length == 0) {
                // If no results are found, send a 404 Not Found response
                connection.release(); // Release the connection back to the pool
                return res.status(404).send("Article not found");
            }
            // Parse the Clauses JSON string into an object
            results[0].Clauses = JSON.parse(results[0].clauses);
            // Send the result as a JSON response with a 200 OK status
            res.status(200).json(results[0]);
            connection.release(); // Release the connection back to the pool
        });
    });
});

// Define a GET endpoint to retrieve all articles and their clauses
app.get('/GetAllArticlesAndClauses', (req, res) => {
    // Get a connection from the pool
    pool.getConnection(function (err, connection) {
        if (err) {
            // Log an error message if there is an error getting a connection
            console.log("Error: " + err);
            connection.release(); // Release the connection back to the pool
            return res.status(500); // Send a 500 Internal Server Error response
        }

        // Define the SQL query to select all articles and their clauses
        let sql = `SELECT *, (SELECT JSON_ARRAYAGG(JSON_OBJECT('English',clauses.ClauseEnglish,'Khmer',clauses.ClauseKhmer,'ID',clauses.ClauseId)) FROM clauses WHERE clauses.ArticleNumber = articles.ArticleNumber) AS clauses FROM articles`;

        // Execute the SQL query
        connection.query(sql, (err, results) => {
            if (err) {
                // Log an error message if there is an error executing the query
                console.log("Error: " + err);
                connection.release(); // Release the connection back to the pool
                return res.status(500).send(err); // Send a 500 Internal Server Error response
            }
            if (results.length == 0) {
                // If no results are found, send a 404 Not Found response
                connection.release(); // Release the connection back to the pool
                return res.status(404).send("Articles not found");
            }

            // Parse the Clauses JSON string into an object for each result
            for (let i = 0; i < results.length; i++) {
                results[i].Clauses = JSON.parse(results[i].clauses);
            }
            // Send the results as a JSON response with a 200 OK status
            res.status(200).json(results);
            connection.release(); // Release the connection back to the pool
        });
    });
});
