function startRemovalTimer(taskId, checkbox) {
    const row = document.getElementById(`task-row-${taskId}`);

    if (checkbox.checked) {
        setTimeout(() => {
            fetch(`/radera_task/${taskId}`, {
                method: 'POST',
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload(); 
                } else {
                    alert("Kunde inte radera.");
                    if (row) row.style.opacity = '1'; 
                    checkbox.checked = false;
                }
            })
            .catch(error => console.error('Error:', error));
        }, 1000); 
    }
}