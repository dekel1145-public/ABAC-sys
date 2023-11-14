# Attribute Based Access Control

This is a simple Authorization System built using FastAPI and Redis.

It allows you to manage user attributes, policies, resources, and perform authorization checks based on policies and user attributes.

## Table of Contents
1. [Set up and Run](#set-up-and-run)
2. [Usage](#usage)
3. [Data Structures in Redis](#data-structures-in-redis)
4. [Scalability](#scalability)

## Set up and Run

### Prerequisites

Before you get started, ensure you have the following prerequisites installed on your system:

* Docker: Docker Installation
* Docker Compose: Docker Compose Installation


### Running the Solution

1. Clone the repository to your local machine:
    ```bash
    git clone abac-dekel
    ```

2. Change your working directory to the project folder:
    ```bash
    cd abac-dekel
    ```

3. Build and start the application and the Redis database using Docker Compose:
    ```bash
    docker-compose up --build -d
    ```
    This command will set up the FastAPI application and a Redis server. The application will be available at http://localhost.

4. To stop the application and the Redis server, use the following command:
    ```bash
    docker-compose down
    ```

## Usage

### APIs

To explore the API endpoints and interact with them, navigate to [http://localhost/docs](http://localhost/docs) in your web browser.

This will provide you with the interactive FastAPI documentation where you can test the endpoints and understand their functionality and body structure.

Feel free to experiment with the provided APIs to manage users, attributes, policies, resources, and authorization according to your requirements.

The solution provides the following APIs:

* Attribute Management:

* * `POST /attributes`: Create a new attribute.
* * `GET /attributes/{attribute_name}`: Retrieve details of a specific attribute by its name.

* User Management:

* * `POST /users`: Create a new user.
* * `GET /users/{user_id}`: Retrieve details of a specific user by their ID.
* * `PUT /users/{user_id}`: Update attributes of a user identified by ID.
* * `PATCH /users/{user_id}/attributes/{attribute_name}`: Update or create the value of a specific attribute of a user.
* * `DELETE /users/{user_id}/attributes/{attribute_name}`: Delete a specific attribute of a user.

* Policy Management:

* * `POST /policies`: Create a new policy.
* * `GET /policies/{policy_id}`: Retrieve details of a specific policy by its ID.
* * `PUT /policies/{policy_id}`: Update conditions of a policy identified by ID.

* Resource Management:

* * `POST /resources`: Create a new resource.
* * `GET /resources/{resource_id}`: Retrieve details of a specific resource by its ID.
* * `PUT /resources/{resource_id}`: Update policy IDs attached to a resource identified by ID.

* Authorization:

* * `GET /is_authorized`: Submit an authorization query to check if a user is authorized to access a resource. Parameters: user_id and resource_id.


## Data Structures in Redis
The solution uses a Redis database to store data. Here's how the data is structured in Redis:

* Attributes: Each attribute is stored as a key-value pair in Redis. The key is `attribute:{attribute_name}`, and the value is the attribute type.

* Users: User attributes are stored as hashes in Redis. Each user's attributes are stored under a key named `user:{user_id}`.

* Policies: Policy conditions are stored as JSON objects. Each policy is stored as a JSON string under a key named `policy:{policy_id}`.

* Resources: Resource policies are stored as sets in Redis. Each resource's policy IDs are stored in an unordered set under a key named `resource:{resource_id}`.


## Scalability
This Authorization System is designed to be highly scalable and can efficiently handle a large number of attributes, users, policies, and resources. Here's how it achieves scalability for your needs:

### Redis as a High-Performance Data Store

Redis is an in-memory data store known for its exceptional performance. It can handle high volumes of data and requests with low latency, making it an ideal choice for scenarios with significant data requirements.

* 1,000 Attributes: Storing attributes in Redis allows for quick retrieval and efficient management of a vast number of attributes. Redis's key-value storage provides rapid access to attribute types, making it easy to validate attributes against policies.

* 10,000 Users: With Redis's capability to manage key-value stores efficiently, user data can be quickly retrieved and modified, even for a large number of users. Redis's in-memory storage allows for rapid access to user attributes, enabling fast authorization checks.

* 10,000 Policies: Storing policy conditions as JSON objects in Redis ensures easy access and modification. Redis's support for complex data structures, such as JSON, helps in managing a vast number of policies effectively.

* 100,000 Resources: Using Redis sets for resource policies makes it efficient to handle a large number of resources. Redis sets are well-suited for managing associations and are optimized for membership checks.

### Asynchronous Operations
FastAPI and the use of asynchronous functions contribute significantly to scalability:

* Concurrency: FastAPI leverages asynchronous programming, enabling the application to handle multiple requests concurrently. This is especially useful in scenarios with a high volume of incoming API requests.

* Non-blocking I/O: Asynchronous functions prevent the application from blocking while waiting for I/O operations, such as reading from Redis. This non-blocking behavior ensures that the system can continue processing other requests while waiting for Redis responses.

* Scalable Architecture: The asynchronous architecture of FastAPI allows the system to make optimal use of available resources, effectively distributing the workload and efficiently managing a large number of incoming requests.

By combining Redis as a high-performance data store and FastAPI's asynchronous capabilities, this solution is well-prepared to meet the demands of managing 1,000 attributes, 10,000 users, 10,000 policies, and 100,000 resources without sacrificing speed or responsiveness.

The system's design allows it to gracefully scale up to meet growing requirements, ensuring a smooth and efficient user experience even as the scale of your application increases.


## Future Improvements

Due to time limitations, the current implementation of the Authorization System provides a solid foundation for managing attributes, users, policies, and resources with high scalability. However, there are opportunities for future enhancements to further improve performance and efficiency. Here are some areas where dynamic programming and caching mechanisms can be applied:

- **Caching for Condition Checks:** Implement a caching mechanism for previously checked conditions to avoid redundant evaluations. When a policy's conditions are checked for a specific user, the result can be cached to reduce the computational overhead for subsequent checks with the same conditions. This can significantly improve the response time for authorization checks.

- **Advanced Resource-User Relationships:** Consider implementing advanced relationship mechanisms between users and resources. By creating links or hierarchies, you can optimize authorization checks for complex scenarios, such as role-based access control, where the user's role hierarchy can be taken into account when determining access to resources.

- **Policy Optimization:** Explore policy optimization techniques to minimize the number of conditions required to make an authorization decision. By reducing the complexity of policies, you can improve performance and reduce the processing time for authorization checks.

- **Machine Learning Integration:** Investigate the integration of machine learning models to enhance authorization decisions. By leveraging historical data and user behavior patterns, machine learning can provide more accurate and adaptive authorization decisions while maintaining scalability.

- **Distributed Caching:** Consider implementing distributed caching solutions, such as Redis or Memcached, to further improve caching capabilities. Distributed caching can enhance performance and provide resilience against high loads.

- **Load Balancing:** Implement load balancing mechanisms to distribute incoming API requests across multiple instances of the Authorization System. Load balancing ensures even distribution of requests, enhancing the system's scalability and reliability.

- **Test Coverage:** Enhance test coverage by adding unit tests and integration tests. Robust testing ensures the reliability and correctness of the system while supporting future development and scaling efforts.

These future improvements, based on dynamic programming principles and caching strategies, can take the Authorization System to the next level of performance and scalability. By optimizing authorization checks and introducing advanced features, the system can adapt to the evolving needs of your application, offering both speed and precision in access control.


## Author

Dekel Levkovich

## License

This project is open-source and available under the MIT License.

