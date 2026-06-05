const express = require("express");
const logger = require("./middleware/logger");

const app = express();

app.use(logger);

app.get("/", (req, res) => {
    res.send("Logging Middleware Working");
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});