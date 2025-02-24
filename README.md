# **Metinvest Digital test task**

## **Project Description**

A system for processing and analyzing inventory data in a warehouse. The project implements data creation, processing,
and analysis using a REST API provided via FastAPI. The system supports asynchronous data processing with Celery and
Redis.

Technology stack: FastAPI, SQLite, Celery, Redis, Pydantic, SQLAlchemy, Docker.

The following effective optimizations were made when working with the database:
- Using Bulk Inserts with SQLAlchemy
- Using Write-Ahead Logging (WAL) for SQLite
- Indexing for Faster Queries
 
More details are provided below in the section: Database Optimization Approaches.

## **Main Features**

- **Fake data generation for inventory items**
- **API for retrieving expense information and popular products**
- **Asynchronous request processing with Celery**
- **Logging and monitoring via Loguru**

---

## **Installation and Setup**

### **1. Clone the repository**

```bash
https://github.com/VolodymyrMamaevsky/Metinvest-task.git
```
Swagger UI will be available at: http://localhost:8000/docs

Command execution examples in this guide for Windows

---

### **2. Create `.env` file**

In the project root, create a `.env` file and add the following environment variables:

```env
DATABASE_URL=sqlite:///./test.db
REDIS_URL=redis://redis:6379
HOST=0.0.0.0
PORT=8000
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
LOG_LEVEL=INFO
DEBUG=False
API_PREFIX=/api
```
---

### **3. Run the Project with Docker**

To run the project using Docker, execute the following command:

```bash
docker-compose up --build
```

This will create all necessary containers:

- **FastAPI** - Your main application.
- **Redis** - Message broker for Celery.
- **Celery** - Handles asynchronous tasks.

---

### **4. Generate Fake Data**

10,000 fake data records will be created in the DB automatically when the Docker is started

---

### **5. Run Tests**

To execute tests, use the command:

```bash
docker-compose run app pytest -v
```
---

## **Database Optimization Approaches**

This project implements several key approaches to optimize database performance, enhancing efficiency and reducing
response times when handling large volumes of data.

#### **1. Using Bulk Inserts with SQLAlchemy**

To speed up data insertion operations, the project utilizes the `bulk_save_objects` method from SQLAlchemy. This method
allows multiple records to be inserted in a single query, significantly reducing overhead compared to inserting
individual records one by one.

📌 *Key Benefits:*

- **Reduced overhead** for multiple insert operations.
- **Faster data processing**, especially for generating large amounts of fake data (e.g., 10,000 orders).

#### **2. Using Write-Ahead Logging (WAL) for SQLite**

The project enables **Write-Ahead Logging (WAL) mode** in SQLite to improve query parallelism. Instead of writing
changes directly to the main database file, SQLite stores them in a separate log file, improving performance.

📌 *Key Benefits:*

- **Faster write and read operations**, especially when multiple transactions are executed simultaneously.
- **Better concurrency**, making it easier to handle high workloads.

#### **3. Indexing for Faster Queries**

The database uses indexes on frequently queried and filtered fields to improve performance.

📌 *Example Indexed Fields:*

- `supplier_id`, `customer_id`, and `order_date` are indexed to speed up queries such as:
    - Retrieving the **top 5 suppliers** by order count.
    - Calculating the **total amount spent** on goods within a specific period.

**Why Indexing Matters?**
Indexes significantly reduce query execution time for large datasets by providing quick access to rows based on indexed
column values.

#### **4. Parallel Asynchronous Data Processing with Celery**

For **asynchronous task processing**, such as updating statistics or creating orders, **Celery** is used with **Redis**
as a message broker.

📌 *Key Benefits:*

- **Offloads heavy data processing** from the main application thread.
- **Improves overall performance** and responsiveness.
- **Handles background tasks efficiently**, ensuring smooth user experience even under high load.

#### **5. Optimized Database Connections**

To efficiently manage database connections, the project utilizes **SQLAlchemy’s connection pooling**. This reduces the
overhead of establishing a new database connection for each query, improving performance.

📌 *Key Benefits:*

- **Minimizes connection overhead**, reducing latency.
- **Ensures efficient resource utilization**, especially under high request loads.

---

## **API Endpoints**
- You can use Postman or Swagger to make requests

### **1. Get Total Expenses for Inventory Over a Period**

- **Method:** `GET`
- **URL:** `/total_spent`

#### **Example GET Request:**

```bash
http://localhost:8000/total_spent?start_date=2025-01-01&end_date=2025-01-31
```

#### **Example Response:**

```json
{
  "total_spent": 105000.25
}
```

---

### **2. Get Top 10 Most Popular Products by Order Volume Over a Period**

- **Method:** `GET`
- **URL:** `/top_products`

#### **Example Get Request:**

```bash
http://localhost:8000/top_products?start_date=2025-01-01&end_date=2025-01-31
```

#### **Example Response:**

```json
{
  "top_products": [
    {
      "product_id": 1,
      "total_quantity": 500
    },
    {
      "product_id": 2,
      "total_quantity": 450
    },
    {
      "product_id": 3,
      "total_quantity": 400
    },
    {
      "product_id": 4,
      "total_quantity": 350
    },
    {
      "product_id": 5,
      "total_quantity": 300
    },
    {
      "product_id": 6,
      "total_quantity": 250
    },
    {
      "product_id": 7,
      "total_quantity": 200
    },
    {
      "product_id": 8,
      "total_quantity": 150
    },
    {
      "product_id": 9,
      "total_quantity": 100
    },
    {
      "product_id": 10,
      "total_quantity": 50
    }
  ]
}
```
### **3. Add a New Order for Inventory**

- **Method:** `POST`
- **URL:** `/create_order`

#### **Example POST Request:**

```bash
http://localhost:8000/docs#/default/create_order_endpoint_create_order_post
```

#### **Request Body (JSON):**

```json
{
  "supplier_id": 1,
  "customer_id": 2,
  "quantity": 100,
  "price": 150.75,
  "order_date": "2025-01-15"
}
```

#### **Example Response:**

```json
{
  "message": "Order added to queue",
  "order_id": 12345
}
```

---

## **Logging**

Logs are stored in the `app_logs.log` file and displayed in the console.
Logs contain details about request execution time, task processing, and errors.

Logging can be configured in `config.py` using **Loguru**.

---

## **Conclusion**

This project effectively implements a system for processing and analyzing inventory data in a warehouse using FastAPI, Celery, and
Redis.

**I hope you will appreciate my efforts** 

**I’d be happy to receive feedback** 😎


