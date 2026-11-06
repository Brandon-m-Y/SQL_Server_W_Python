-- Create the Orders table. If it already exists, skip this and keep its data.
-- 'U' means only look for a table with this name.
-- NOT NULL means every row must have a value in that column.
IF OBJECT_ID('dbo.Orders', 'U') IS NULL
CREATE TABLE dbo.Orders (
    OrderID INT CONSTRAINT PK_Orders PRIMARY KEY NOT NULL,  -- whole number, unique for each row
    OrderDate DATE NOT NULL,                                 -- date only, no time
    CustomerName NVARCHAR(100) NOT NULL,                     -- text, up to 100 characters
    Product NVARCHAR(100) NOT NULL,                          -- text, up to 100 characters
    Amount DECIMAL(10, 2) NOT NULL                           -- number with 2 decimal places
);


/*
For testing: use this instead of the IF above to start with an empty table
on every run. It deletes the table and all its data, then recreates it.

DROP TABLE IF EXISTS dbo.Orders;

CREATE TABLE dbo.Orders (
    ...
);
*/
