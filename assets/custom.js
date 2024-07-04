
document.addEventListener('change', function(e) {
    if (e.target && e.target.id === 'file_upload') {
        const file = e.target.files[0];
        if (file) {
            const event = new CustomEvent('file_selected', {
                detail: {
                    path: file.path || file.webkitRelativePath || file.name,
                    name: file.name,
                    size: file.size,
                    type: file.type
                }
            });
            document.dispatchEvent(event);
        }
    }
});
