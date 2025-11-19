# tehisintellekt.ee test assignment

# Project Overview

This project is an example full-stack application to demonstrate the usage of the requirements set in the job listing. It consists of a **React/Next.js frontend**, a **FastAPI backend**, containerized with **Docker**, and deployed within the **Microsoft Azure** ecosystem.
---

## Live example
The (example production) application is deployed in the **Microsoft Azure ecosystem**

[https://tehisintellekt.sven.spot](https://tehisintellekt.sven.spot)


Please note that due to infrastructure constraints of the demo app, the first load can be a little slow - this is not an issue with the webapp itself!

## Tech Stack

### **Frontend**
- NodeJS v20
- React.js
- Next.js
- TailwindCSS
- TypeScript 

### **Backend**
- Python3.14
- FastAPI
- OpenAI API & Gemini API Integrations

### **Infrastructure & running the project**
- Containerized using **Docker** for both frontend and backend  
- Orchestrated locally with **docker-compose**
- Environment variables used for configuration

To run the project, just clone the repository and run:

`docker compose up`

Note that the backend is currently integrated to two AI services:
1. OpenAI API
2. Gemini API

Either one or both of them can be used, but at least one is needed to make the app work. In the future more integrations can be added.

---

## Environment Variables

Both the frontend and backend use environment variables for configuration.  
Below are example values you can adjust as needed.

### **Backend (`backend/.env`)**
```
# 1 for dev, leave blank for production
DEV=
# your OpenAI API key
OPENAI_API_KEY=
# which model to use or leave blank if you want to use the default
OPENAI_MODEL=
# your Gemini API key, leave blank if you don't want to use it
GEMINI_API_KEY=
# which model to use or leave blank if you want to use the default
GEMINI_MODEL=
```

### **Frontend (`frontend/.env`)**
```
# Backend API base URL, http://localhost:8000 by default
NEXT_PUBLIC_BACKEND_URL=
```
