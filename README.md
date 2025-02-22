# **Metinvest Digital test task**

## **Project Description**

A system for processing and analyzing inventory data in a warehouse. The project implements data creation, processing,
and analysis using a REST API provided via FastAPI. The system supports asynchronous data processing with Celery and
Redis.

## **Main Features**

- **Fake data generation** for inventory items.
- **API for retrieving expense information** and **popular products**.
- **Asynchronous request processing** with Celery.
- **Logging and monitoring** via Loguru.

---

## **Installation and Setup**

### **1. Install Dependencies**

To install all project dependencies, use Poetry (if Poetry is not installed, install it using the command below):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Now, install all dependencies:

```bash
poetry install
```

---

### **2. Create a `.env` File**

In the project root, create a `.env` file and add the following environment variables:

```env
DATABASE_URL=sqlite:///./test.db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
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

The FastAPI container will be available on **port 8000**.

---

### **4. Generate Fake Data**

To generate fake inventory data in the database, run:

```bash
poetry run python -m app.models.generate_fake_data
```

This will create **10,000 records** in the database.

---

### **5. Run Tests**

To execute tests, use the command:

```bash
pytest -v
```

---

## **Database Optimization Approaches**

This project implements several key approaches to optimize database performance, enhancing efficiency and reducing
response times when handling large volumes of data.

### **1. Using Bulk Inserts with SQLAlchemy**

To speed up data insertion operations, the project utilizes the `bulk_save_objects` method from SQLAlchemy. This method
allows multiple records to be inserted in a single query, significantly reducing overhead compared to inserting
individual records one by one.

📌 **Key Benefits:**

- **Reduced overhead** for multiple insert operations.
- **Faster data processing**, especially for generating large amounts of fake data (e.g., 10,000 orders).

### **2. Using Write-Ahead Logging (WAL) for SQLite**

The project enables **Write-Ahead Logging (WAL) mode** in SQLite to improve query parallelism. Instead of writing
changes directly to the main database file, SQLite stores them in a separate log file, improving performance.

📌 **Key Benefits:**

- **Faster write and read operations**, especially when multiple transactions are executed simultaneously.
- **Better concurrency**, making it easier to handle high workloads.

### **3. Indexing for Faster Queries**

The database uses indexes on frequently queried and filtered fields to improve performance.

📌 **Example Indexed Fields:**

- `supplier_id`, `customer_id`, and `order_date` are indexed to speed up queries such as:
    - Retrieving the **top 5 suppliers** by order count.
    - Calculating the **total amount spent** on goods within a specific period.

**Why Indexing Matters?**
Indexes significantly reduce query execution time for large datasets by providing quick access to rows based on indexed
column values.

### **4. Parallel Asynchronous Data Processing with Celery**

For **asynchronous task processing**, such as updating statistics or creating orders, **Celery** is used with **Redis**
as a message broker.

📌 **Key Benefits:**

- **Offloads heavy data processing** from the main application thread.
- **Improves overall performance** and responsiveness.
- **Handles background tasks efficiently**, ensuring smooth user experience even under high load.

### **5. Optimized Database Connections**

To efficiently manage database connections, the project utilizes **SQLAlchemy’s connection pooling**. This reduces the
overhead of establishing a new database connection for each query, improving performance.

📌 **Key Benefits:**

- **Minimizes connection overhead**, reducing latency.
- **Ensures efficient resource utilization**, especially under high request loads.

---

## **API Endpoints**

### **1. Get Total Expenses for Inventory Over a Period**

- **Method:** `GET`
- **URL:** `/total_spent`

#### **Example Request:**

```bash
GET /total_spent?start_date=2025-01-01&end_date=2025-01-31
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

#### **Example Request:**

```bash
GET /top_products?start_date=2025-01-01&end_date=2025-01-31
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

---

## **Logging**

Logs are stored in the `app_logs.log` file and displayed in the console.
Logs contain details about request execution time, task processing, and errors.

Logging can be configured in `config.py` using **Loguru**.

---

## **Conclusion**

This project implements a system for processing and analyzing inventory data in a warehouse using **FastAPI, Celery, and
Redis**.

✔ **All data is automatically generated and stored in a SQLite database.**  
✔ **You can interact with the system via a REST API.**  
✔ **Celery handles asynchronous task processing efficiently.**  


