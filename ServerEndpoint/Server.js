const express = require('express');
const mysql = require('mysql');

const app = express();
const port = 3000;

const connectionConfig = {
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'khmerpenalcode'
};

//Here we create a connection pool to help with the connection to the database
let pool = mysql.createPool(connectionConfig);


//We also allow the application to use json as the data format
app.use(express.json());

// Start the server
app.listen(port, function (err) {
    if (err) {
        console.log("Error in server setup");
    } else {
        console.log(`Server running on port`, port);
    }
});

// Define a GET endpoint to query the database
app.get('/GetCrimes', (req, res) => {
    pool.getConnection(function (err, connection) {
        if (err) {
            console.log("Error: " + err);
            connection.release();
            return res.status(500).send(err);
        }

        let sql = 'SELECT * FROM crime';

        connection.query(sql, function (err, results) {
            if (err) {
                console.log("Error: " + err);
                connection.release();
                return res.status(500).send(err);
            }
            if (results.length == 0) {
                return res.status(404).send("Crimes not found");
            }
            res.status(200).json(results);
            connection.release();
        });
    });
});

app.get('/GetCrime', (req, res) => {
    if (req.query.ID == null) {
        return res.status(400).send("ID is required");
    }
    pool.getConnection(function (err, connection) {       
        if (err) {
            console.log("Error: " + err);
            connection.release();
            return res.status(500).send(err);
        }

        let sql = `SELECT * FROM crime WHERE ID = ${req.query.ID}`;

        connection.query(sql, function (err, results) {
            if (err) {
                console.log("Error: " + err);
                connection.release();
                return res.status(500).send(err);
            }
            if (results.length == 0) {
                return res.status(404).send("Crimes not found");
            }
            res.status(200).json(results[0]);
            connection.release();
        });
    });
});

app.get('/GetAggrivationAndClausesFromCrime', (req, res) => {
    var ID = req.query.ID;
    if (ID == null) {
        return res.status(400).send("Crime ID is required");
    }

    pool.getConnection(function (err, connection) {
        if (err) {
            console.log("Error: " + err);
            connection.release();
            return res.status(500)
        }
        let sql = `SELECT * FROM aggrivations INNER JOIN clauses ON aggrivations.ClauseID = clauses.ClauseId WHERE CrimeID = ${ID}`;

        connection.query(sql, (err, results) => {
            if (err) {
                console.log("Error: " + err);
                connection.release();
                return res.status(500).send(err);
            }
            if (results.length == 0) {
                return res.status(404).send("Aggrivations not found");
            }
            res.status(200).json(results);
            connection.release();
        });
    });
});

app.get('/GetArticleAndClauses', (req, res) => {
    var ID = req.query.Article;
    if (ID == null) {
        return res.status(400).send("Article is required");
    }

    pool.getConnection(function (err, connection) {
        if (err) {
            console.log("Error: " + err);
            connection.release();
            return res.status(500)
        }

        let sql = `SELECT *, (SELECT JSON_ARRAYAGG(JSON_OBJECT('English',clauses.ClauseEnglish,'Khmer',clauses.ClauseKhmer,'ID',clauses.ClauseId)) FROM Clauses WHERE clauses.ArticleNumber = articles.ArticleNumber) AS Clauses FROM articles WHERE articles.ArticleNumber = ${ID}`;

        connection.query(sql, (err, results) => {
            if (err) {
                console.log("Error: " + err);
                connection.release();
                return res.status(500).send(err);
            }
            if (results.length == 0) {
                return res.status(404).send("Article not found");
            }
            results[0].Clauses = JSON.parse(results[0].Clauses);
            res.status(200).json(results[0]);
            connection.release();
        });
    });
});

app.get('/GetAllArticlesAndClauses', (req, res) => {
    pool.getConnection(function (err, connection) {
        if (err) {
            console.log("Error: " + err);
            connection.release();
            return res.status(500)
        }

        let sql = `SELECT *, (SELECT JSON_ARRAYAGG(JSON_OBJECT('English',clauses.ClauseEnglish,'Khmer',clauses.ClauseKhmer,'ID',clauses.ClauseId)) FROM Clauses WHERE clauses.ArticleNumber = articles.ArticleNumber) AS Clauses FROM articles`;

        connection.query(sql, (err, results) => {
            if (err) {
                console.log("Error: " + err);
                connection.release();
                return res.status(500).send(err);
            }
            if (results.length == 0) {
                return res.status(404).send("Articles not found");
            }

            for (let i = 0; i < results.length; i++) {
                results[i].Clauses = JSON.parse(results[i].Clauses);
            }
            res.status(200).json(results);
            connection.release();
        });
    });
});
