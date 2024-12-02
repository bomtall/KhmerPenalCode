const express = require('express');
const mysql = require('mysql');


const app = express();
const port = 3000;

const connectionConfig = {
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'kmherpenalcode'
};

//Here we create a connection pool to help with the connection to the database
var pool = mysql.createPool(connectionConfig);


//We also allow the application to use json as the data format
app.use(express.json());

// Start the server
app.listen(port, function (err) {
    if (err) {
        console.log("Error in server setup");
    } else {
        console.log(`Server running on port ${port}`);
    }
});

// Define a GET endpoint to query the database
app.get('/get-crimes', (req, res) => {
    var ID = req.query.ID;

    pool.getConnection(function (err, connection) {
        if (err) {
            console.log(err);
        }

        let sql = 'SELECT * FROM crime'; // Replace 'your_table_name' with your actual table name
        connection.query(sql, function (err, results) {
            if (err) {
                console.log("Error: " + err);
                connection.release();
                return res.status(500).send(err);
            }
            res.status(200).json(results);
            connection.release();
        });
    });
});


app.get('/get-aggrivation-and-clauses-From-crime', (req, res) => {
    var ID = req.query.ID;
    let sql = 'SELECT * FROM aggrivations WHERE CrimeID = ID'; // Replace 'your_table_name' with your actual table name
    db.query(sql, (err, results) => {
        if (err) {
            return res.status(500).send(err);
        }
        res.json(results);
    });
});

app.get('/get-article-and-clauses', (req, res) => {
    var ID = req.query.ID;
    let sql = `SELECT * FROM articles WHERE ID = ${ID}`; // Replace 'your_table_name' with your actual table name
    db.query(sql, (err, results) => {
        if (err) {
            return res.status(500).send(err);
        }
        res.json(results);
    });
});
