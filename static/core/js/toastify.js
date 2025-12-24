function showToast(message, type) {
    Toastify({
        text: message,
        className: type,
        gravity: 'top',
        position: 'center',
        stopOnFocus: true,
        duration: 2000,
        close: true,
        style: {
            background: get_message_color(type),
        },
    }).showToast();
}

// Function for color mapping logic
function get_message_color(value) {
    if (value === 'info') {
        return '#417caf';
    } else if (value === 'warning') {
        return '#816a42';
    } else if (value === 'error') {
        return '#a94442';
    } else if (value === 'success') {
        return '#5f9460';
    } else {
        return '#31708f';
    }
}
