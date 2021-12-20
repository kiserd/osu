
/*
    SETUP
*/

// Express
var express = require('express');                           // We are using the express library for the web server
var app     = express();                                    // We need to instantiate an express object to interact with the server in our code
app.use(express.static(__dirname + '/public'));             // potentially may need to add public css/html/images at some point
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
const PORT        = process.env.PORT || 5000;                // Set a port number at the top so it's easy to change in the future

// Handlebars
var handlebars = require('express-handlebars').create({
    defaultLayout:'main',
    helpers: {
        ifEquals: function (id1, id2) { return id1 == id2; },
      }
});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

// Database
// var db = require('./db-connector');
const {Pool} = require('pg');
const pool = new Pool({
  connectionString: "postgres://zrlxljmqdkvszr:68f3caa6c05eac373403f310b61d1c8299d012f7cfa6502e70704f9b71442cbf@ec2-34-200-94-86.compute-1.amazonaws.com:5432/d5g9fhqn80h10u",
  ssl: {
    rejectUnauthorized: false
  }
});

/*
    QUERY STRINGS
*/

// SELECT
const selectAllCustomers = 'SELECT * FROM customers';
const selectAllProducts = 'SELECT * FROM products';
const selectAllGiftcards = 'SELECT * FROM gift_cards';
const selectAllPurchases = 'SELECT * FROM purchases';
const selectAllPurchasesProducts = 'SELECT * FROM purchases_products ORDER BY purchase_product_id';
const selectPurchaseDetails =   `SELECT
                                p.purchase_id,
                                p.customer_id,
                                pp.product_id,
                                pp.quantity,
                                p.date
                            
                                FROM
                                purchases p
                                LEFT JOIN purchases_products pp
                                ON p.purchase_id = pp.purchase_id`;

// SELECT - for dynamic filter component
const selectLastNames = 'SELECT DISTINCT name_last FROM customers ORDER BY name_last';
const selectDescriptions = 'SELECT DISTINCT description FROM products ORDER BY description';
const selectCustomerIdDropDown = 'SELECT DISTINCT customer_id, name_first, name_last FROM customers ORDER BY customer_id';

// SELECT - for dynamic drop downs in entering records
const selectProductIds = 'SELECT DISTINCT product_id, description FROM products ORDER BY product_id';
const selectPurchaseIds = 'SELECT DISTINCT purchase_id, name_first, name_last FROM purchases LEFT JOIN customers ON purchases.customer_id = customers.customer_id ORDER BY purchase_id';

// INSERT
const insertCustomer = 'INSERT INTO customers(name_first, name_last, email) VALUES($1, $2, $3)';
const insertProduct = 'INSERT INTO products(description, price, stock) VALUES($1, $2, $3)';
const insertPurchase = 'INSERT INTO purchases(customer_id, date) VALUES($1, $2)';
const insertGiftcard = 'INSERT INTO gift_cards(customer_id, total_price, total_used) VALUES($1, $2, $3)';
const insertGiftcardNullCID = 'INSERT INTO gift_cards(total_price, total_used) VALUES($1, $2)';
const insertPurchaseProduct = 'INSERT INTO purchases_products(purchase_id, product_id, quantity) VALUES($1, $2, $3)';

// DELETE
const deleteCustomer = 'DELETE FROM customers WHERE customer_id = ($1)';
const deleteProduct = 'DELETE FROM products WHERE product_id = ($1)';
const deletePurchase = 'DELETE FROM purchases WHERE purchase_id = ($1)';
const deleteGiftcard = 'DELETE FROM gift_cards WHERE gift_card_id = ($1)';
const deletePurchaseProduct = 'DELETE FROM purchases_products WHERE purchase_product_id = ($1)';

// UPDATE
const updateCustomer = 'UPDATE customers SET name_first = ($1), name_last = ($2), email = ($3) WHERE customer_id= ($4)';
const updateProduct = 'UPDATE products SET description = ($1), price = ($2), stock = ($3) WHERE product_id= ($4)';
const updatePurchase = 'UPDATE purchases SET customer_id = ($1), date = ($2) WHERE purchase_id= ($3)';
const updateGiftcard = 'UPDATE gift_cards SET customer_id = ($1), total_price = ($2), total_used = ($3) WHERE gift_card_id= ($4)';
const updateGiftcardNullCID = 'UPDATE gift_cards SET customer_id = NULL, total_price = ($1), total_used = ($2) WHERE gift_card_id= ($3)';
const updatePurchaseProduct = 'UPDATE purchases_products SET purchase_id = ($1), product_id = ($2), quantity = ($3) WHERE purchase_product_id= ($4)';

/*
    HELPER FUNCTIONS
*/

var convertDate = function(date) {
  var myDate = new Date(date);
  var month = myDate.getMonth() + 1;
  var day = myDate.getDate();
  var monthStr = '';
  var dayStr = '';
  // add '0' padding to single digit month
  if (month < 10) {
    monthStr = '0' + month;
  }
  else {
    monthStr = '' + month;
  }
  // add '0' padding to single digit day
  if (day < 10) {
    dayStr = '0' + day;
  }
  else {
    dayStr = '' + day;
  }
  
  var dateString = myDate.getFullYear() + '-' + monthStr + '-' + dayStr;
  return dateString;
}

/*
    ROUTES
*/

// home page handler
app.get('/', (req, res) => {
    res.render('index.handlebars');
});

// purchases and products route handler
app.get('/purchasesproducts', (req, res) => {
    var context = {};

    // setup DELETE if delete requested
    var deleteString = 'SELECT customer_id FROM customers WHERE customer_id = ($1)'; // dummy query
    var values = [1];
    if (req.query.delete) {
        deleteString = deletePurchaseProduct;
        values = [req.query.delete];
        context.deleteMessage = "DELETE SUCCESS: Deleted Purchase Product ID " + req.query.delete;
        context.deleteSuccessFlag = 1;
    }

    // delete row/record if applicable
    pool.query(deleteString, values, (err, queryRes) => {
        // get M:M linker table data
        pool.query(selectAllPurchasesProducts, (err, queryRes) => {
            context.pp = queryRes.rows;
            // get 1:M purchases table data
            pool.query(selectAllPurchases, (err, queryRes) => {
                context.purchases = queryRes.rows;
                // get 1:M products table data
                pool.query(selectAllProducts, (err, queryRes) => {
                    context.products = queryRes.rows;
                    // get distinct product_id for drop-down
                    pool.query(selectProductIds, (err, queryRes) => {
                        context.product_ids = queryRes.rows;
                        // get distinct purchase_id for drow down
                        pool.query(selectPurchaseIds, (err, queryRes) => {
                            context.purchase_ids = queryRes.rows;
                            res.render('purchasesproducts.handlebars', context);
                        });
                    });
                });
            });
        });
    });
});

// purchases and products INSERT post route handler
// ** work to reduce callback hell down the road **
app.post('/purchasesproducts', (req, res) => {
    var context = {};

    // setup INSERT if applicable
    var insertString = 'SELECT customer_id FROM customers'; // dummy query
    var insValues = [];
    if (req.body.insert) {
        var purchaseIDIsNull = req.body.purchase_id === '';
        var productIDIsNull = req.body.product_id === '';
        var quantityIsNull = req.body.quantity === '';
        if (!purchaseIDIsNull && !productIDIsNull && !quantityIsNull) {
            insertString = insertPurchaseProduct;
            insValues = [req.body.purchase_id, req.body.product_id, req.body.quantity];
            context.insertMessage = "INSERT SUCCESS: Added Purchase ID #" + req.body.purchase_id + ", Product ID #" + req.body.product_id;
            context.insertSuccessFlag = 1;
        }
        else {
            context.insertError = "INSERT ERROR: Neither Purchase ID, Product ID, or Quantity can be NULL";
            context.insertErrorFlag = 1;
        }
    }

    // setup UPDATE if applicable
    var updateString = 'SELECT customer_id FROM customers'; // dummy query
    var updValues = [];
    if (req.body.update) {
        var purchaseIDIsNull = req.body.purchase_id === '';
        var productIDIsNull = req.body.product_id === '';
        var quantityIsNull = req.body.quantity === '';
        if (!purchaseIDIsNull && !productIDIsNull && !quantityIsNull) {
            updateString = updatePurchaseProduct;
            updValues = [req.body.purchase_id, req.body.product_id, req.body.quantity, req.body.update];
            context.updateMessage = "UPDATE SUCCESS: Updated Purchase Product ID #" + req.body.update;
            context.updateSuccessFlag = 1;
        }
        else {
            context.updateError = "UPDATE ERROR: Neither Purchase ID, Product ID, or Quantity can be NULL";
            context.updateErrorFlag = 1;
        }
    }

    // update record if applicable
    pool.query(updateString, updValues, (err, queryRes) => {
        // insert into M:M table
        pool.query(insertString, insValues, (err, queryRes) => {
            // get M:M linker table data
            pool.query(selectAllPurchasesProducts, (err, queryRes) => {
                context.pp = queryRes.rows;
                // get 1:M purchases table data
                pool.query(selectAllPurchases, (err, queryRes) => {
                    context.purchases = queryRes.rows;
                    // get 1:M products table data
                    pool.query(selectAllProducts, (err, queryRes) => {
                        context.products = queryRes.rows;
                        // get distinct product_id for drop-down
                        pool.query(selectProductIds, (err, queryRes) => {
                            context.product_ids = queryRes.rows;
                            // get distinct purchase_id for drow down
                            pool.query(selectPurchaseIds, (err, queryRes) => {
                                context.purchase_ids = queryRes.rows;
                                res.render('purchasesproducts.handlebars', context);
                            });
                        });
                    });
                });
            });
        });
    });
});

// customers page basic get route handler
app.get('/customers', (req, res) => {
    var context = {};

    // setup WHERE clause if filter provided
    var selectString = selectAllCustomers;
    // alter query string if filter provided
    if (req.query.filter) {
        selectString += " WHERE name_last = " + "'" + req.query.filter + "'";
    }
    selectString += " ORDER BY customer_id";

    // setup DELETE if delete requested
    var deleteString = 'SELECT customer_id FROM customers'; // dummy query
    var values = [];
    if (req.query.delete) {
        deleteString = deleteCustomer;
        values = [req.query.delete];
        context.deleteMessage = "DELETE SUCCESS: Deleted Customer ID " + req.query.delete;
        context.deleteSuccessFlag = 1;
    }

    // delete customer if applicable
    pool.query(deleteString, values, (err, queryRes) => {
        // get distinct last names to populate filter
        pool.query(selectLastNames, (err, queryRes) => {
            context.filter_values = queryRes.rows;
            // populate context with select query results
            pool.query(selectString, (err, queryRes) => {
                context.rows = queryRes.rows;
                // render template and pass context
                res.render('customers.handlebars', context);
            });
        });
    });
});

// customers INSERT post route handler
app.post('/customers', (req, res) => {
    var context = {};

    // setup INSERT if applicable
    var insertString = 'SELECT customer_id FROM customers'; // dummy query
    var insValues = [];
    if (req.body.insert) {
        var firstNameIsNull = req.body.name_first === '';
        var lastNameIsNull = req.body.name_last === '';
        if (!firstNameIsNull && !lastNameIsNull) {
            insertString = insertCustomer;
            insValues = [req.body.name_first, req.body.name_last, req.body.email];
            context.insertMessage = "INSERT SUCCESS: Added " + req.body.name_first + " " + req.body.name_last;
            context.insertSuccessFlag = 1;
        }
        else {
            context.insertError = "INSERT ERROR: Neither First Name or Last Name can be NULL";
            context.insertErrorFlag = 1;
        }
    }

    // setup UPDATE if applicable
    var updateString = 'SELECT customer_id FROM customers'; // dummy query
    var updValues = [];
    if (req.body.update) {
        var firstNameIsNull = req.body.name_first === '';
        var lastNameIsNull = req.body.name_last === '';
        if (!firstNameIsNull && !lastNameIsNull) {
            updateString = updateCustomer;
            updValues = [req.body.name_first, req.body.name_last, req.body.email, req.body.update];
            context.updateMessage = "UPDATE SUCCESS: Updated Customer ID #" + req.body.update;
            context.updateSuccessFlag = 1;
        }
        else {
            context.updateError = "UPDATE ERROR: Neither First Name or Last Name can be NULL";
            context.updateErrorFlag = 1;
        }
    }

    // setup SELECT string
    var selectString = selectAllCustomers + " ORDER BY customer_id";

    // update record if applicable
    pool.query(updateString, updValues, (err, queryRes) => {
        // handle potential UPDATE error
        if (err) {
            context.updateSuccessFlag = 0;
            context.updateErrorFlag = 1;
            context.updateError = "UPDATE ERROR: unspecified SQL error"
        }
        // insert into customers table
        pool.query(insertString, insValues, (err, queryRes) => {
            // get distinct last names to populate filter
            pool.query(selectLastNames, (err, queryRes) => {
                context.filter_values = queryRes.rows;
                // get new customers table to populate template
                pool.query(selectString, (err, queryRes) => {
                    context.rows = queryRes.rows;
                    res.render('customers.handlebars', context);
                });
            });
        });
    });
});

// add product page handler
app.get('/products', (req, res) => {
    context = {};

    // setup filter if argument provided
    var selectString = selectAllProducts;
    // alter query string if filter provided
    if (req.query.filter) {
        selectString += " WHERE description = " + "'" + req.query.filter + "'";
    }
    selectString += " ORDER BY product_id";

    // setup DELETE if delete requested
    var deleteString = 'SELECT customer_id FROM customers'; // dummy query
    var values = [];
    if (req.query.delete) {
        deleteString = deleteProduct;
        values = [req.query.delete];
        context.deleteMessage = "DELETE SUCCESS: Deleted Product ID " + req.query.delete;
        context.deleteSuccessFlag = 1;
    }

    // delete row/record if applicable
    pool.query(deleteString, values, (err, queryRes) => {
        // get distinct descriptions for dynamic filter
        pool.query(selectDescriptions, (err, queryRes) => {
            context.filter_values = queryRes.rows;
            // get table rows to display to user
            pool.query(selectString, (err, queryRes) => {
                context.rows = queryRes.rows;
                res.render('products.handlebars', context);
            });
        });
    });
});

// products INSERT post route handler
app.post('/products', (req, res) => {
    var context = {};

    // setup INSERT if applicable
    var insertString = 'SELECT customer_id FROM customers'; // dummy query
    var insValues = [];
    if (req.body.insert) {
        var descriptionIsNull = req.body.description === '';
        var priceIsNull = req.body.price === '';
        var stockIsNull = req.body.stock === '';
        if (!descriptionIsNull && !priceIsNull && !stockIsNull) {
            insertString = insertProduct;
            insValues = [req.body.description, req.body.price, req.body.stock];
            context.insertMessage = "INSERT SUCCESS: Added " + req.body.description;
            context.insertSuccessFlag = 1;
        }
        else {
            context.insertError = "INSERT ERROR: Neither Description, Price, or Stock can be NULL";
            context.insertErrorFlag = 1;
        }
    }

    // setup UPDATE if applicable
    var updateString = 'SELECT customer_id FROM customers'; // dummy query
    var updValues = [];
    if (req.body.update) {
        var descriptionIsNull = req.body.description === '';
        var priceIsNull = req.body.price === '';
        var stockIsNull = req.body.stock === '';
        if (!descriptionIsNull && !priceIsNull && !stockIsNull) {
            updateString = updateProduct;
            updValues = [req.body.description, req.body.price, req.body.stock, req.body.update];
            context.updateMessage = "UPDATE SUCCESS: Updated Product ID# " + req.body.update;
            context.updateSuccessFlag = 1;
        }
        else {
            context.updateError = "UPDATE ERROR: Neither Description, Price, or Stock can be NULL";
            context.updateErrorFlag = 1;
        }
    }

    // setup SELECT string
    var selectString = selectAllProducts + " ORDER BY product_id";

    // update record if applicable
    pool.query(updateString, updValues, (err, queryRes) => {
        // insert into products table
        pool.query(insertString, insValues, (err, queryRes) => {
            // get distinct descriptions for dynamic filter
            pool.query(selectDescriptions, (err, queryRes) => {
                context.filter_values = queryRes.rows;
                // get new products table to populate template
                pool.query(selectString, (err, queryRes) => {
                    context.rows = queryRes.rows;
                    res.render('products.handlebars', context);
                });
            });
        });
    });
});

// add purchase page handler
app.get('/purchases', (req, res) => {
    context = {};

    // setup filter query string if applicable
    var selectString = selectAllPurchases;
    // alter query string if filter provided
    if (req.query.filter) {
        selectString += " WHERE customer_id = " + "'" + req.query.filter + "'";
    }
    selectString += " ORDER BY purchase_id";

    // setup DELETE if delete requested
    var deleteString = 'SELECT customer_id FROM customers'; // dummy query
    var values = [];
    if (req.query.delete) {
        deleteString = deletePurchase;
        values = [req.query.delete];
        context.deleteMessage = "DELETE SUCCESS: Deleted Purchase ID " + req.query.delete;
        context.deleteSuccessFlag = 1;
    }

    // delete row/record if applicable
    pool.query(deleteString, values, (err, queryRes) => {
        // get distinct customer_id for dynamic filter drop-down
        pool.query(selectCustomerIdDropDown, (err, queryRes) => {
            context.filter_values = queryRes.rows;
            // get table rows to display to user
            pool.query(selectString, (err, queryRes) => {
                var rows = queryRes.rows;
                // convert dates to mm/dd/yyyy
                for (var i = 0; i < rows.length; i++) {
                    rows[i]["date"] = convertDate(rows[i]["date"]);
                }
                context.rows = rows;
                res.render('purchases.handlebars', context);
            });
        });
    });
});

// purchases INSERT post route handler
app.post('/purchases', (req, res) => {
    var context = {};

    // setup INSERT if applicable
    var insertString = 'SELECT customer_id FROM customers'; // dummy query
    var insValues = [];
    if (req.body.insert) {
        var customerIDIsNull = req.body.customer_id === '';
        var dateIsNull = req.body.date === '';
        if (!customerIDIsNull && !dateIsNull) {
            insertString = insertPurchase;
            insValues = [req.body.customer_id, req.body.date];
            context.insertMessage = "INSERT SUCCESS: Added New Purchase";
            context.insertSuccessFlag = 1;
        }
        else {
            context.insertError = "INSERT ERROR: Neither Customer ID or Date can be NULL";
            context.insertErrorFlag = 1;
        }
    }

    // setup UPDATE if applicable
    var updateString = 'SELECT customer_id FROM customers'; // dummy query
    var updValues = [];
    if (req.body.update) {
        var customerIDIsNull = req.body.customer_id === '';
        var dateIsNull = req.body.date === '';
        if (!customerIDIsNull && !dateIsNull) {
            updateString = updatePurchase;
            updValues = [req.body.customer_id, req.body.date, req.body.update];
            context.updateMessage = "UPDATE SUCCESS: Updated Purchase ID# " + req.body.update;
            context.updateSuccessFlag = 1;
        }
        else {
            context.updateError = "UPDATE ERROR: Neither Customer ID or Date can be NULL";
            context.updateErrorFlag = 1;
        }
    }

    // setup SELECT string
    var selectString = selectAllPurchases + " ORDER BY purchase_id";

    // update record if applicable
    pool.query(updateString, updValues, (err, queryRes) => {
        // insert into purchases table
        pool.query(insertString, insValues, (err, queryRes) => {
            // get distinct customer_id for dynamic filter drop-down
            pool.query(selectCustomerIdDropDown, (err, queryRes) => {
                context.filter_values = queryRes.rows;
                // get new purchases table to populate template
                pool.query(selectString, (err, queryRes) => {
                    var rows = queryRes.rows;
                    // convert dates to mm/dd/yyyy
                    for (var i = 0; i < rows.length; i++) {
                        rows[i]["date"] = convertDate(rows[i]["date"]);
                    }
                    context.rows = rows;
                    res.render('purchases.handlebars', context);
                });
            });
        });
    });
});

var convertGiftcardNulls = function(context) {
    // loop through query results and replace true null with 'NULL' string
    for (var i = 0; i < context.rows.length; i++) {
        if (context.rows[i].customer_id == null) {
            context.rows[i].customer_id = 'NULL';
        }
    }
    return context;
}

// giftcards GET page handler
app.get('/giftcards', (req, res) => {
    context = {}

    // setup filter query string if applicable
    var selectString = selectAllGiftcards;
    // alter query string if filter provided
    if (req.query.filter) {
        selectString += " WHERE customer_id = " + "'" + req.query.filter + "'";
    }
    selectString += " ORDER BY gift_card_id";

    // setup DELETE if delete requested
    var deleteString = 'SELECT customer_id FROM customers WHERE customer_id = ($1)'; // dummy query
    var values = [1];
    if (req.query.delete) {
        deleteString = deleteGiftcard;
        values = [req.query.delete];
        context.deleteMessage = "DELETE SUCCESS: Deleted Giftcard ID " + req.query.delete;
        context.deleteSuccessFlag = 1;
    }

    // delete row/record if applicable
    pool.query(deleteString, values, (err, queryRes) => {
        // get distinct customer_id for dynamic filter drop-down
        pool.query(selectCustomerIdDropDown, (err, queryRes) => {
            context.filter_values = queryRes.rows;
            context.filter_values.push({customer_id: 'NULL', name_first: 'NULL'});
            // get table records to display to user
            pool.query(selectString, (err, queryRes) => {
                context.rows = queryRes.rows;
                context = convertGiftcardNulls(context);
                res.render('giftcards.handlebars', context);
            });
        });
    });
});



// giftcards INSERT post route handler
app.post('/giftcards', (req, res) => {
    var context = {};

    // setup INSERT if applicable
    var insertString = 'SELECT customer_id FROM customers'; // dummy query
    var insValues = [];
    if (req.body.insert) {
        var priceIsNull = req.body.total_price === '';
        var usedIsNull = req.body.total_used === '';
        if (!priceIsNull && !usedIsNull) {
            insertString = insertGiftcard;
            insValues = [req.body.customer_id, req.body.total_price, req.body.total_used];
            if (!req.body.customer_id || req.body.customer_id === 'NULL') {
                insertString = insertGiftcardNullCID;
                insValues = [req.body.total_price, req.body.total_used];
            }
            context.insertMessage = "INSERT SUCCESS: Added Giftcard for Customer ID " + req.body.customer_id;
            context.insertSuccessFlag = 1;
        }
        else {
            context.insertError = "INSERT ERROR: Neither Price or Used can be NULL";
            context.insertErrorFlag = 1;
        }
    }

    // setup UPDATE if applicable
    var updateString = 'SELECT customer_id FROM customers'; // dummy query
    var updValues = [];
    if (req.body.update) {
        var priceIsNull = req.body.total_price === '';
        var usedIsNull = req.body.total_used === '';
        if (!priceIsNull && !usedIsNull) {
            updateString = updateGiftcard;
            updValues = [req.body.customer_id, req.body.total_price, req.body.total_used, req.body.update];
            if (!req.body.customer_id || req.body.customer_id === 'NULL') {
                updateString = updateGiftcardNullCID;
                updValues = [req.body.total_price, req.body.total_used, req.body.update];
            }
            context.updateMessage = "UPDATE SUCCESS: Updated Giftcard ID " + req.body.update;
            context.updateSuccessFlag = 1;
        }
        else {
            context.updateError = "UPDATE ERROR: Neither Price or Used can be NULL";
            context.updateErrorFlag = 1;
        }
    }

    // setup SELECT string
    var selectString = selectAllGiftcards + " ORDER BY gift_card_id";

    // update record if applicable
    pool.query(updateString, updValues, (err, queryRes) => {
        // insert into giftcards table
        pool.query(insertString, insValues, (err, queryRes) => {
            // get distinct customer_id for dynamic filter drop-down
            pool.query(selectCustomerIdDropDown, (err, queryRes) => {
                context.filter_values = queryRes.rows;
                context.filter_values.push({customer_id: 'NULL', name_first: 'NULL'});
                // get new giftcards table to populate template
                pool.query(selectString, (err, queryRes) => {
                    context.rows = queryRes.rows;
                    context = convertGiftcardNulls(context);
                    res.render('giftcards.handlebars', context);
                });
            });
        });
    });
});


/*
    LISTENER
*/

// This is the basic syntax for what is called the 'listener' which receives incoming requests on the specified PORT.
app.listen(PORT, function(){
    console.log('Express started on http://localhost:' + PORT + '; press Ctrl-C to terminate.')
});