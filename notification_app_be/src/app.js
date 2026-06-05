const express = require("express");

const notificationRoutes = require("./routes/notificationRoutes");

const app = express();

app.use(express.json());

app.use("/api/v1/notifications", notificationRoutes);

app.listen(5000, () => {
    console.log("Notification Service Running");
});