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
var pool  = mysql.createPool(connectionConfig);


//We also allow the application to use json as the data format
app.use(express.json());


// Connect to the database
db.connect((err) => {
    if (err) {
        throw err;
    }
    console.log('Connected to database');
});

// Define a GET endpoint to query the database
app.get('/get-crimes', (req, res) => {
    var ID = req.query.ID;
    let sql = 'SELECT * FROM crimes'; // Replace 'your_table_name' with your actual table name
    db.query(sql, (err, results) => {
        if (err) {
            return res.status(500).send(err);
        }
        res.json(results);
    });
});


app.get('/get-aggrivations', (req, res) => {
    var ID = req.query.ID;
    let sql = 'SELECT * FROM crimes'; // Replace 'your_table_name' with your actual table name
    db.query(sql, (err, results) => {
        if (err) {
            return res.status(500).send(err);
        }
        res.json(results);
    });
});


app.post();

// Start the server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});