# Cloud Service Access Management System

Team Members: Emmanuel Ifeanyi, Josue Cota, Nathan Chen

This application is a FastAPI-based backend system to manage access to cloud services 
based on user subscriptions. It provides role-based access control (RBAC), 
usage tracking, and enforcement of API limits.

## Features:
1. **Subscription Plan Management**
2. **Permission Management**
3. **User Subscription Handling**
4. **Access Control**
5. **Usage Tracking and Limit Enforcement**

---

## Prerequisites

Ensure you have the following installed:
- **Python 3.9+**
- **MongoDB Atlas** (or any MongoDB instance)
- **Pip** (Python package manager)

---

## 1. Project Setup

### a. Clone the Repository:
git clone https://github.com/PencilknightZX/Cloud-Access-Hub.git

##2. Install Dependencies:
using pip install these:
fastapi
uvicorn
motor
pydantic

##3. Configure MongoDB
Setup MongoDB Connection
create an .env file and add your mongo_uri, ex: MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority
Replace <username>, <password>, <cluster>, and <dbname> with your MongoDB Atlas credentials


##4. Run the Application
Use this command in your terminal:
uvicorn main:app --reload


##5. Test Endpoints
Use Postman to test endpoints
Example requests are listed in Requests.txt 



