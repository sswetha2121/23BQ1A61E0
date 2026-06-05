const express = require("express");

const {
    createNotification,
    getNotifications,
    markAsRead
} = require("../controllers/notificationController");

const router = express.Router();

router.post("/", createNotification);
router.get("/:userId", getNotifications);
router.patch("/:notificationId/read", markAsRead);

module.exports = router;