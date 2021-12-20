-- **************************************************************************
-- THIS FILE WILL COMPLETELY REFRESH THE DATABASE
-- DO NOT RUN THIS UNLESS YOU WANT TO LOSE SUBSEQUENT TRANSACTIONS
-- **************************************************************************

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS gift_cards;
DROP TABLE IF EXISTS purchases_products;
SET FOREIGN_KEY_CHECKS = 1;

--
-- table structure for table `customers`
--
CREATE TABLE `customers` (
`customer_id` int(11) NOT NULL AUTO_INCREMENT,
`name_first` varchar(255) NOT NULL,
`name_last` varchar(255) NOT NULL,
`email` varchar(255) DEFAULT NULL,
PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB;

--
-- dumping data for table `customers`
--
INSERT INTO
`customers` (`name_first`, `name_last`, `email`)

VALUES
('Han', 'Solo', 'han.solo@gmail.com'),
('Dennis', 'Reynolds', 'dennis.reynolds@gmail.com'),
('Joe', 'Lauzon', 'joe.lauzon@aol.com'),
('Mike', 'Perry', 'mike.perry@gmail.com'),
('Robert', 'Whittaker', 'rob.whittaker@hotmail.com');


--
-- table structure for table `products`
--
CREATE TABLE `products` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `price` decimal(5, 2) NOT NULL,
  `stock` int(11) UNSIGNED NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB;

--
-- Dumping data for table `products`
--
INSERT INTO
`products` (`description`, `price`, `stock`)

VALUES
('Premium Dog Chow', 100.00, 3),
('Budget Dog Chow', 50.00, 2),
('Premium Cat Chow', 50.00, 4),
('Budget Cat Chow', 25.00, 3),
('Small Dog Toy', 5.00, 3),
('Medium Dog Toy', 10.00, 2),
('Large Dog Toy', 15.00, 6),
('Small Cat Toy', 2.50, 3),
('Large Cat Toy', 5.00, 1);


--
-- table structure for table `gift_cards`
--
CREATE TABLE `gift_cards` (
  `gift_card_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `total_price` decimal(5, 2) UNSIGNED NOT NULL,
  `total_used` decimal(5, 2) UNSIGNED NOT NULL,
  PRIMARY KEY (`gift_card_id`),
  CONSTRAINT `customer_fk` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

--
-- Dumping data for table `gift_cards`
--
INSERT INTO
`gift_cards` (`customer_id`, `total_price`, `total_used`)

VALUES
(1, 100.00, 100.00),
(3, 50.00, 20.00),
(4, 50.00, 0.00),
(1, 25.00, 0.00),
(2, 75.00, 75.00),
(2, 100.00, 50.00);


--
-- table structure for table `purchases`
--
CREATE TABLE `purchases` (
  `purchase_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`purchase_id`),
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

--
-- Dumping data for table `purchases`
--
INSERT INTO
`purchases` (`customer_id`, `date`)

VALUES
(1, '2020-12-15'),
(1, '2021-01-17'),
(4, '2020-11-14'),
(1, '2020-10-08'),
(2, '2020-09-09'),
(2, '2021-02-25');


--
-- table structure for table `purchases_products`
--
CREATE TABLE `purchases_products` (
  `purchase_product_id` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) UNSIGNED NOT NULL,
  PRIMARY KEY (`purchase_product_id`),
  CONSTRAINT `purchase_fk` FOREIGN KEY (`purchase_id`) REFERENCES `purchases` (`purchase_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `product_fk` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

--
-- Dumping data for table `purchases_products`
--
INSERT INTO
`purchases_products` (`purchase_id`, `product_id`, `quantity`)

VALUES
(1, 1, 1),
(1, 5, 2),
(1, 6, 1),
(2, 2, 2),
(3, 3, 2),
(3, 4, 1),
(3, 3, 2),
(4, 5, 1),
(5, 1, 2),
(5, 3, 2),
(6, 4, 1),
(6, 9, 1);
