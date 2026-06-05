const {
    create,
    getAll,
    markRead
} = require("../services/notificationService");

exports.createNotification = (req, res) => {
    res.json(create(req.body));
};

exports.getNotifications = (req, res) => {
    res.json(getAll(req.params.userId));
};

exports.markAsRead = (req, res) => {
    res.json(markRead(req.params.notificationId));
};