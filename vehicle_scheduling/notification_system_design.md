# Notification System Design

# Stage 1 – API Design

## Create Notification

POST /api/v1/notifications

Request

```json
{
  "title": "Placement Drive",
  "message": "Amazon hiring for 2027 batch",
  "type": "placement",
  "priority": "high",
  "targetUsers": ["user1", "user2"]
}
```

Response

```json
{
  "notificationId": "notif_001",
  "status": "created"
}
```

## Get Notifications

GET /api/v1/users/{userId}/notifications

Response

```json
{
  "notifications": [
    {
      "id": "notif_001",
      "title": "Placement Drive",
      "message": "Amazon hiring for 2027 batch",
      "priority": "high",
      "isRead": false
    }
  ]
}
```

## Mark Notification as Read

PATCH /api/v1/notifications/{notificationId}/read

Response

```json
{
  "status": "read"
}
```

---

# Stage 2 – Database Design

## Users Table

| Column     | Type         |
| ---------- | ------------ |
| user_id    | UUID         |
| name       | VARCHAR(100) |
| email      | VARCHAR(255) |
| created_at | TIMESTAMP    |

## Notifications Table

| Column          | Type         |
| --------------- | ------------ |
| notification_id | UUID         |
| title           | VARCHAR(255) |
| message         | TEXT         |
| type            | VARCHAR(50)  |
| priority        | VARCHAR(20)  |
| created_at      | TIMESTAMP    |

## UserNotifications Table

| Column          | Type      |
| --------------- | --------- |
| id              | UUID      |
| user_id         | UUID      |
| notification_id | UUID      |
| is_read         | BOOLEAN   |
| delivered_at    | TIMESTAMP |

Indexes

```sql
CREATE INDEX idx_users_email ON users(email);

CREATE INDEX idx_notifications_created_at
ON notifications(created_at);

CREATE INDEX idx_user_notifications_user
ON user_notifications(user_id);
```

---

# Stage 3 – Query Optimization

Strategies:

* Use indexing on user_id and notification_id.
* Use pagination for large notification lists.
* Avoid SELECT * queries.
* Use caching for frequently accessed notifications.
* Use database connection pooling.
* Optimize joins with indexed foreign keys.

Example Query

```sql
SELECT n.notification_id,
       n.title,
       n.message,
       un.is_read
FROM notifications n
JOIN user_notifications un
ON n.notification_id = un.notification_id
WHERE un.user_id = ?
ORDER BY n.created_at DESC
LIMIT 20;
```

---

# Stage 4 – Performance Improvements

* Redis caching for recent notifications.
* Database indexing.
* Load balancing across API servers.
* Asynchronous notification processing.
* Horizontal scaling using microservices.
* WebSocket connections for real-time updates.

---

# Stage 5 – Reliable Bulk Notifications

Architecture:

1. Producer Service creates notification.
2. Message Queue (Kafka/RabbitMQ) stores jobs.
3. Worker Services consume jobs.
4. Notifications delivered asynchronously.
5. Retry mechanism for failed deliveries.
6. Dead Letter Queue for persistent failures.

Benefits:

* High throughput
* Fault tolerance
* Retry support
* Better scalability

---

# Stage 6 – Priority Inbox Algorithm

Priority Score Calculation

Priority Score =
(Urgency × 5)

* (User Relevance × 3)
* (Recency × 2)

Example:

Placement Alert

Urgency = 10

Relevance = 9

Recency = 8

Priority Score

= (10×5)+(9×3)+(8×2)

= 50+27+16

= 93

Notifications are sorted in descending order of Priority Score.

Time Complexity:

O(n log n)

using sorting algorithms.
