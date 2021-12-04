


create table "Customer"(
    "customerID" int(10) AUTO_INCREMENT PRIMARY KEY,
    "customerPassword" varchar(50) not null,
    "customerName" varchar(50) not null,
    "customerEmail" varchar(50),
    "balance" int(20) not null,
    primary key("customerID")

)

create table "Product"(
    "productID" int(10) AUTO_INCREMENT PRIMARY KEY,
    "productOwner" int(10) not null,
    "productName" varchar(50) not null,
    "productDescription" varchar(1000) not null,
    "status" varchar(50) check "status" in ("to_be_verified", "verified", "rejected", "in_auction", "unpaid", "paid", "payment_expired", "abortive", "deleted"),
    primary key("productID"),
    foreign key ("productOwner") references "Customer"("customerID")

)


create table "transaction"(
    "transactionID" int(10) AUTO_INCREMENT PRIMARY KEY,
    "product" int(10) not null,
    "buyer" int(10) not null,
    "transactionStatus" varchar(50) check "transactionStatus" in ("paid", "unpaid"),
    primary key("transactionID"),
    foreign key ("buyer") references "Customer"("customerID"),
    foreign key ("product") references "Product"("productID")
)

create table "Admin"(
    "adminID" int(10) AUTO_INCREMENT PRIMARY KEYl,
    "adminPassword" varchar(50) not null,
    "adminPassword" varchar(50) not null,
    "adminName" varchar(50) not null,
    primary key("AdminID")
)