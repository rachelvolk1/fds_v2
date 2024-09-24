window.onload = function() {
    const section = document.querySelector('.section');
    section.style.display = 'block';
};
(document).ready(function() {
    // Initialize DataTable
    var table = $('#yourTableId').DataTable(); // Replace with your actual table ID

    // Handle form submission
    $('#uploadForm').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this); // Create FormData object from the form

        $.ajax({
            url: $(this).attr('action'), // URL for the file upload
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                table.clear(); // Clear existing data

                // Add new rows to DataTable
                if (response.data && Array.isArray(response.data)) {
                    table.rows.add(response.data).draw();
                } else {
                    $('#error-message').text('Unexpected data format received.');
                }
            },
            error: function(err) {
                console.error('Error uploading file:', err);
                $('#error-message').text('Error uploading file. Please try again.');
            }
        });
    });

    // Optional: Preview file contents before uploading
    $('#file-upload').on('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var contents = e.target.result;
                // Display file contents in #data-preview for previewing
                $('#data-preview').text(contents);
                // Optionally parse CSV data here and show a preview
            };
            reader.readAsText(file);
        }
    });

    // Ensure the section is displayed when the page loads
    const section = document.querySelector('.section');
    if (section) {
        section.style.display = 'block';
    }
});

