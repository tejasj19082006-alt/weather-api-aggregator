# weather-api-aggregator

# 🌦️ Weather API Aggregator - Week 1

A high-performance, asynchronous backend service built with **FastAPI** designed to aggregate data from external weather providers. This project follows production-grade backend engineering practices, demonstrating rigorous configuration security, virtual environment isolation, and professional Git version control management.

---

## 📁 Week 1: Project Architecture & Directory Layout

During the initial phase of development, we established a strict modular design pattern to enforce separation of concerns. This ensures that our core routing logic remains clean and scalable for future integrations:

```text
weather-api-aggregator/
│
├── app/                        # Main Application Package Directory
│   ├── __init__.py             # Marks directory as a Python package
│   └── main.py                 # Application Bootstrap and Core Routing
│
├── venv/                       # Isolated Local Python Virtual Environment
├── .env                        # Local Environment Variables (Strictly Private)
├── .gitignore                  # Git Exclusion Criteria Engine
├── README.md                   # Comprehensive System Documentation
└── requirements.txt            # Explicit Dependency Declaration Record

# 🌦️ Weather API Aggregator - Week 2

A comprehensive overview of our second development milestone. This week focused heavily on architectural decoupling, high-performance asynchronous networking, external API integration, and real-world editor environment troubleshooting.

---

## 📁 Week 2: Directory Architecture Expansion

To maintain a clean codebase, we expanded our application directory by introducing a dedicated `services` package. This physically separates our network logic from our web routing logic.

```text
weather-api-aggregator/
│
├── app/                        
│   ├── services/               # NEW: Encapsulated Business & Network Logic
│   │   ├── __init__.py         # Marks 'services' as a Python sub-package
│   │   └── weather.py          # NEW: Asynchronous OpenWeatherMap Client
│   ├── __init__.py             
│   └── main.py                 # UPDATED: Ingests the WeatherService
│
├── venv/                       # Active Virtual Environment
├── .env                        # Secure Credentials
└── requirements.txt            # Dependency Manifest