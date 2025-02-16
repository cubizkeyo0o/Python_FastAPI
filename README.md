Clean Architecture

-API/: Contains API endpoints.

    +Models/: Defines data models used in the API.
    +Routers/v1/: Contains route handlers for versioned API endpoints.
  
  
-Application/: Manages application logic and business services.

    +AppServices/: Implements business logic and application services.
    +Dtos/: Contains Data Transfer Objects (DTOs) for request/response handling.

  
-Domain/Entities/: Defines domain models and core business entities.


-Infrastructure/: Handles data persistence and configuration.

    +Config/: Manages environment settings and database configurations.
    +Repositories/: Contains repository classes for database operations.
  
main.py: The entry point of the application.

Package: SQLAlchemy, uvicorn, pydantic, fastapi
