let notifications = [];

exports.create = (data) => {
    notifications.push(data);
    return {
        message: "Notification Created",
        data
    };
};

exports.getAll = () => {
    return notifications;
};

exports.markRead = (id) => {
    return {
        notificationId: id,
        status: "read"
    };
};