var express = require('express');
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});
var session = require('express-session');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var math = require('math');
var mysql = require('./dbcon.js');

app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(session({secret: "secretPassword"}));
app.use(express.static(__dirname + '/public'));

app.set('port', 6032);

const selectAllQuery = 'SELECT * FROM shoppingList';
const selectUnpurchasedQuery = "SELECT * FROM shoppingList WHERE purchased=0";
const insertQuery = "INSERT INTO shoppingList (`name`, `qty`, `price`, `purchased`) VALUES (?)";
const deleteQuery = "DELETE FROM shoppingList WHERE id=?";
const updateQuery = "UPDATE shoppingList SET name=?, done=?, due=? WHERE id=? ";
const dropTableQuery = "DROP TABLE IF EXISTS shoppingList";
const makeTableQuery = `CREATE TABLE shoppingList(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(255) NOT NULL,
                        qty INT,
                        price INT,
                        purchased BOOLEAN);`;
const makeProductTableQuery = `CREATE TABLE products(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(255) NOT NULL,
                        price INT);`;
const updatePurchasedQuery = "UPDATE shoppingList SET purchased=1 WHERE id=?";


// app.get('/insertProduct', (req, res, next) => {
//   var vals = ['Smart Sticks', 11];
//   mysql.pool.query("INSERT INTO products (`name`, `price`) VALUES (?)", [vals], (err, result) => {
//     if(err){
//       next(err);
//       return;
//     }
//     res.render('food.handlebars');
//   });
// });

app.get('/markPurchased', (req, res, next) => {
  var id = req.query.id;
  mysql.pool.query(updatePurchasedQuery, req.query.id, (err, result) => {
    if(err){
      next(err);
      return;
    }
    res.send("success");
  });
});

app.get('/insert', (req, res, next) => {
  var vals = [];
  vals.push(req.query.name);
  vals.push(req.query.qty);
  mysql.pool.query("SELECT price FROM products WHERE `name`=?", req.query.name, (err, rows, fields) =>{
    if(err){
      next(err);
      return;
    }
    var price = rows[0]["price"] * req.query.qty;
    vals.push(price);
    vals.push(0);
    mysql.pool.query(insertQuery, [vals], (err, result) => {
      if(err){
        next(err);
        return;
      }
      res.render('food.handlebars', context);
    });
  }); 
});

app.get('/getUnpurchased', (req, res, next) => {
  context = {};
  mysql.pool.query(selectUnpurchasedQuery, (err, rows, fields) => {
    if(err){
      next(err);
      return;
    }
    res.send(rows);
  });
});

app.get('/reset-table', (req, res, next) => {
  var context = {};
  mysql.pool.query(dropTableQuery, (err) => {
    mysql.pool.query(makeTableQuery, function(err){
      context.results = "Table reset";
      res.render('food.handlebars',context);
    })
  });
});

// app.get('/makeProductTable', (req, res, next) => {
//   mysql.pool.query(makeProductTableQuery, (err) => {
//     res.render('food.handlebars');
//   });
// });

app.get('/', (req, res) => {
  res.render('index.handlebars');
});

app.get('/terms', (req, res) => {
  res.render('terms.handlebars');
});

app.get('/food', (req, res, next) => {
  context = {};
  mysql.pool.query(selectUnpurchasedQuery, (err, rows, fields) => {
    if(err){
      next(err);
      return;
    }
    context.rows = rows;
    res.render('food.handlebars', context);
  });
});

app.get('/exercise', (req, res) => {
  res.render('exercise.handlebars');
});

app.post('/exercise', (req, res) => {
  var appID = "c80f52c3a805d68e0ce5bf34b5b33fb8";
  var urlAndQueryString = "https://api.openweathermap.org/data/2.5/weather?q=98087,us&appid=";
  var fullResource = urlAndQueryString + appID;
  //console.log(fullResource);
  var request = new XMLHttpRequest();
  request.open("GET", fullResource, false);
  request.send(null);
  var response = JSON.parse(request.responseText);
  //console.log(response);
  var tempKelvin = response["main"]["temp"];
  var tempF = math.round((tempKelvin - 273.15) * 9/5 + 32);
  //console.log(tempF);
  var mainWeather = response["weather"][0]["main"];
  //console.log(mainWeather);
  var detailWeather = response["weather"][0]["description"];
  //console.log(detailWeather);
  weatherArr = [];
  weatherArr.push({"key" : "Temp F", "value" : tempF});
  weatherArr.push({"key" : "Main Weather", "value" : mainWeather});
  weatherArr.push({"key" : "Detailed Weather", "value" : detailWeather});
  var context = {};
  context.weatherStuff = weatherArr;
  res.render('exercise.handlebars', context);
})

app.get('/grooming', (req, res) => {
  context = {};
  context.tester = "get tester";
  res.render('grooming.handlebars', context);
});

app.post('/grooming', (req, res) => {
  var context = req.body;
  res.send(context);
});

app.use(function(req,res){
  res.status(404);
  res.render('404');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});

app.listen(app.get('port'), function(){
  console.log(`Express started on http://${process.env.HOSTNAME}:${app.get('port')}; press Ctrl-C to terminate.`);
});