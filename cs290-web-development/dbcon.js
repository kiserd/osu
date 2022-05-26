var mysql = require('mysql');
var pool = mysql.createPool({
  connectionLimit : 10,
  host            : 'cs290-web-development.cfwbm0mzgsgn.us-west-2.rds.amazonaws.com',
  port            : '3306',
  user            : 'admin',
  password        : 'password',
  database        : 'main'
});

// var pool = mysql.createConnection({
  // connectionLimit : 10,
  // host            : 'cs290-web-development.cfwbm0mzgsgn.us-west-2.rds.amazonaws.com',
  // port            : '3306',
  // user            : 'admin',
  // password        : 'password',
  // database        : 'cs290-web-development',
  // ssl             : true
// });

// pool.connect(function(err) {
//   if (err) {
//     console.error('Database connection failed: ' + err.stack);
//     return;
//   }

//   console.log('Connected to database.');
// });

// pool.end();

module.exports.pool = pool;