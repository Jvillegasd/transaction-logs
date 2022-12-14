# Transaction logs

  

This project consist in create a simple bank transaction system, where users can interact with their transactions and filter them. `Python 3.10` was used for this project.

  

## Requirements

  

- As a user I want to be able to login and see the transactions, listed from most recent to least recent.

- As a user I can return my balance as a mathematical result of the executed transactions.

- As a user I want to be able to list the transactions in a range of dates.

- As a user I want to be able to list the transactions by type.

- As a user I want to be able to filter the expenses by merchant.

  

## System requirements

  

- You must ensure that a user cannot see the transactions of other users

- There are three types of transactions in this simple system which are deposits, withdrawals and expenses.

- he results of the transactions must be paged being the page size passed as a query parameter, if no parameter present then assume 10 as page size

- You cannot withdraw/waste more money than the account has, therefore negative balances are not allowed.

- If a transaction results in a negative balance, it must be rejected.

- Validate that the date ranges make sense for the transaction filter.

  

## Data importer

CRUD for transactions is not required, instead, I designed and developed a data importer class that loads seeds in JSON files for the models created for the project. This DataImporter class was designed as a generic way to loads models seeds, so it is reusable.

  

## Persist data

  

Loaded seeds are stored in a local `PostgreSQL` database mounted by `Docker` (you can see this service in details in docker compose file), so backend can interact with the data through queries.

  

## Sessions

  

In order to maintain sessions for logged users, a simple session provided for Flask was used.

  

## Libraries

  

A core rule was to do not use external libraries for the project beyond the framework. So, I chose Flask as Backend micro-framework and SQLAlchemy as ORM library (Unlike Django or FastAPI, Flask lacks of ORM). Schemas, filters, serializers are made from vanilla, my own implementations.

  

## Documentation

  

Core functions, method and classes have their own docstring for code documentation. API Postman collection is saved in folder `docs` inside repo.

  

## Unit testing

  

Python in-build library `unittest` was used for implement unit tests for this backend. I implemented different test cases for API endpoints and DataImporter in order to cover most cases. Tests inherit from a `BaseCase` class that implement common functions that all tests can use. This class allows unit tests to load models seeds on demand. You can execute tests with the following command:

  

python3 -m unittest

If you use Docker for run this project, you can run tests with this command:

  

docker exec transaction-api python3 -m unittest

  

## Run the project

  

In order to make easier to run this project in multiple environment, a Docker image and a Docker compose file were created. You can build and run this project with this command:

  

docker-compose up -d

  

## Environment variables

On this section, you can see how an Environment vars file looks like:

    APP_ENV=dev
    PORT=3001
    SECRET_KEY=u3gsKSs8QSSdOXkw6nxB9Gq2xuCF8UQ6
    
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=admin123
    POSTGRES_HOST=transaction-db
    POSTGRES_PORT=5432
    POSTGRES_DB=transaction-logs-db

## Filtering

A vanilla filtering algorithm was created for handle dynamic filters for ORM queries. For complex filtering such as range comparison, I implemented a bracket notation to accomplish this. On the following table, you will see the available filtering notation. Filters are received as Query parameters!

 - For direct filter, use normal query parameter notation, example:
	 - `GET - /api/transactions?transaction_type=expense`
 - For range filtering, you have these operations:
	 - '[lt]' = 'Lower than'
	- '[le]' = 'Lower or equal than'
	- '[gt]' = 'Greater than'
	- '[ge]' = 'Greater or equal than'
	- '[eq]' = 'Equals to'
	 - Example: `GET - /api/transactions?created_at[ge]=12-15-2022&created_at[le]=12-25-2022`
 - PD: Dates have format: `month-day-year`

## Pagination
Pagination is handle via Query parameters using Cursor technique for quick database queries. The cursor is the field `created_at` in timestamp. Example:

    GET - /api/transactions?per_page=5&next_cursor=1671112380.617523
You can combine pagination with filters queries!