Clean Architecture

-API/: Contains API endpoints.

    +Routers/v1/: Contains route handlers for versioned API endpoints.
    +Tags: group and describe API endpoints related.
  
-Application/: Manages application logic and business services.

    +AppServices/: Implements business logic and application services.
    +Models/: Defines data models used in the API.

-Domain/: Manages application logic and business services.

    +Entities/: Defines domain models and core business entities.
    +Base/: Defines base models for entities.

-Infrastructure/: Handles data persistence and configuration.

    +Config/: Manages environment settings and database configurations.
    +Repositories/: Contains repository classes for database operations.
    +database/: Setup migration and init session dbcontext
  
main.py: The entry point of the application.

Package: SQLAlchemy, uvicorn, pydantic, fastapi
