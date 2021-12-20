

-- SELECT
-- basic SELECT queries to populate table data on various pages
-- note: the dynamic filter dropdowns are populated using these by extracting
--       specific fields from the rows using the handlebars templating engine
SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM purchases;
SELECT * FROM gift_cards;
SELECT * FROM purchases_products;


-- INSERT
-- basic INSERT queries used to add new rows to tables
INSERT INTO customers (name_first, name_last, email) VALUES (:fnameInput, :lnameInput, :emailInput);
INSERT INTO products (description, price, stock) VALUES (:descInput, :priceInput, :stockInput);
INSERT INTO purchases (customer_id, date) VALUES (:custInput, :dateInput);
INSERT INTO gift_cards (customer_id, total_price, total_used) VALUES (:custInput, :priceInput, :usedInput);
INSERT INTO purchases_products (purchase_id, product_id, quantity) VALUES (:purchInput, :prodInput, :quantityInput);


-- DELETE
-- basic DELETE queries to remove entire record from table
DELETE FROM customers WHERE id = :idInput;
DELETE FROM products WHERE id = :idInput;
DELETE FROM purchases WHERE id = :idInput;
DELETE FROM gift_cards WHERE id = :idInput;
DELETE FROM purchases_products WHERE id = :idInput;


-- UPDATE
-- basic UPDATE queries to alter records in table
UPDATE customers SET name_first = :fnameInput, name_last = :lnameInput, email = :emailInput WHERE id= :idInput;
UPDATE products SET description = :descInput, price = :priceInput, stock = :stockInput WHERE id= :idInput;
UPDATE purchases SET customer_id = :custInput, date = :dateInput WHERE id= :idInput;
UPDATE gift_cards SET customer_id = :custInput, total_price = :priceInput, total_used = :usedInput WHERE id= :idInput;
UPDATE purchases_products SET purchase_id = :purchInput, product_id = :prodInput, quantity = :quantityInput WHERE id= :idInput;


-- SELECT
-- more advanced SELECT queries using JOINs to gather more meaningful data
-- or to filter data

-- get customers by last name
SELECT
*
FROM
customers
WHERE
name_last = :nameInput;

-- get products by description
SELECT
*
FROM
products
WHERE
description = :descInput;

-- get purchases by customer_id
SELECT
*
FROM
purchases
WHERE
customer_id = :custInput;

-- get giftcards by customer_id
SELECT
*
FROM
gift_cards
WHERE
customer_id = :custInput;

-- giftcard balance by customer
SELECT
c.customer_id,
c.name_first,
c.name_last,
SUM(gc.total_price) - SUM(gc.total_used) AS gc_balance

FROM
customers c
LEFT JOIN gift_cards gc
ON c.customer_id = gc.customer_id

GROUP BY
c.customer_id,
c.name_first,
c.name_last;

-- total price by purchase and customer name
SELECT
pu.purchase_id,
c.customer_id,
c.name_first,
c.name_last,
pp.quantity * pr.price AS total_price,

FROM purchases pu
LEFT JOIN customers c
ON pu.customer_id = c.customer_id
LEFT JOIN purchases_products pp
ON pu.purchase_id = pp.purchase_id
LEFT JOIN products pr
ON pp.product_id = pr.product_id

GROUP BY
pu.purchase_id,
c.customer_id,
c.name_first,
c.name_last;
