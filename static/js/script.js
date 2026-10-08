document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alertBox) {
        setTimeout(() => {
            alertBox.remove();
        }, 5000);
    });
});
