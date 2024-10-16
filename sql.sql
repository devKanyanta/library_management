CREATE DATABASE IF NOT EXISTS mySchoolLibrary;

USE mySchoolLibrary;

CREATE TABLE IF NOT EXISTS Publishers (
    publisherID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Authors (
    authorID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Books (
    bookID INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    publisherID INT,
    yearPublished INT,
    FOREIGN KEY (publisherID) REFERENCES Publishers(publisherID)
);

CREATE TABLE IF NOT EXISTS Students (
    studentID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(45) NOT NULL,
    phone VARCHAR(45),
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Librarian (
    librarianID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(45),
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS BookAuthors (
    bookID INT,
    authorID INT,
    PRIMARY KEY (bookID, authorID),
    FOREIGN KEY (bookID) REFERENCES Books(bookID),
    FOREIGN KEY (authorID) REFERENCES Authors(authorID)
);

CREATE TABLE IF NOT EXISTS Loans (
    loanID INT PRIMARY KEY AUTO_INCREMENT,
    bookID INT,
    studentID INT,
    borrowDate DATE NOT NULL,
    dueDate DATE NOT NULL,
    returnDate DATE,
    FOREIGN KEY (bookID) REFERENCES Books(bookID),
    FOREIGN KEY (studentID) REFERENCES Students(studentID)
);

CREATE TABLE IF NOT EXISTS LoanRequests (
    requestID INT PRIMARY KEY AUTO_INCREMENT,
    studentID INT,
    bookID INT,
    requestDate DATE NOT NULL DEFAULT CURRENT_DATE,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (studentID) REFERENCES Students(studentID),
    FOREIGN KEY (bookID) REFERENCES Books(bookID)
);