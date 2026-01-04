Live Demo: View the Dashboard Here

<img width="1619" height="669" alt="image" src="https://github.com/user-attachments/assets/d1265d6e-3f48-4d52-a7d2-3cb5b2d8a73e" />


NYC Taxi Analytics Platform : 

This project is a comprehensive data engineering and analytics solution designed to process and analyze large-scale urban transportation data. Using the New York City Taxi & Limousine Commission (TLC) dataset, I built a system that transforms millions of raw trip records into a dynamic dashboard providing actionable insights into city wide revenue and passenger behavior.

Project Overview : 

The objective of this platform is to answer critical business questions for transportation stakeholders, such as identifying high revenue geographic areas, determining peak service hours, and understanding tipping patterns. The system manages the entire data lifecycle, from initial ingestion and structural cleaning in a cloud data warehouse to the final delivery of an interactive visual interface.

Technical Architecture: 

The platform is built on a modern data stack that emphasizes scalability and performance:

Data Warehouse: Snowflake serves as the central engine for storage and computation. I organized the data into a multi layered structure (Raw and Analytics layers) to separate original source data from refined business logic.

Analytical Layer: I developed a series of SQL views that handle complex calculations, such as converting microsecond-precision timestamps into readable formats and performing multi table joins to map location IDs to actual neighborhood names.

User Interface: A Streamlit application built in Python provides a live connection to the warehouse. This interface allows users to filter millions of rows of data instantaneously through a web browser.

Key Features : 

Dynamic Geographic Filtering: Users can drill down into specific boroughs to view localized performance metrics.

Temporal Trend Analysis: The platform identifies peak demand by hour, allowing for a better understanding of when services are most utilized throughout a 24 hour cycle.

Automated Summarization: By using pre aggregated data layers, the dashboard remains fast and responsive, even when processing several million records.

Data Integrity: The pipeline includes filters to remove incomplete records and "Unknown" locations, ensuring that all reported insights are based on accurate, high-quality data.

Business Impact : 

By analyzing over 3 million individual trips, this platform reveals significant operational trends:

Revenue Concentration: Financial analysis identifies Manhattan as the primary revenue driver, while highlighting emerging demand in other boroughs.

Peak Demand Windows: Detailed hourly tracking shows a consistent city-wide spike in activity between 6:00 PM and 8:00 PM, providing a clear target for resource optimization.

High-Value Service Areas: The platform specifically tracks high-tipping neighborhoods, offering insights into where premium service demand is strongest.

How to Use This Project : 

1- Code Repository: Clone the repository to your local environment.

2- Environment Setup: Install the necessary Python libraries listed in the requirements file.

3- Database Configuration: Execute the provided SQL scripts in a Snowflake environment to establish the necessary table structures and views.

4- Application Launch: Run the Streamlit command to open the interactive dashboard in your local browser.
