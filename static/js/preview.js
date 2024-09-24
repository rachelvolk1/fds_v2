window.onload = function() {
    const section = document.querySelector('.section');
    section.style.display = 'block';
};

$(document).ready(function() {
    var filename = "{{ filename|tojson }}";  // Ensure Flask variable is safely passed into JS

    if (filename) {
        // Initialize DataTable with AJAX to fetch data from Flask endpoint
        var table = $('#dataTable').DataTable({
            paging: true,
            searching: true,  // Activate search
            ordering: true,   // Activate column sorting
            info: true,       // Activate info at the bottom
            pageLength: 10,   // Set default page length
            lengthMenu: [10, 25, 50, 100],  // Options for page length
            ajax: {
                url: `/api/preview/${filename}`,  // API route to fetch the dataset
                dataSrc: '',  // Assuming the data is a flat array of objects
                error: function(xhr, status, error) {
                    $('#status-message').text('Error loading dataset: ' + error);
                }
            },
            columns: [
                { data: 'TPIN', title: 'TPIN' },
                { data: 'LOCATION', title: 'Location' },
                { data: 'TAX TYPE', title: 'Tax Type' },
                { data: 'Transaction ID', title: 'Transaction ID' },
                { data: 'Period From', title: 'Period From' },
                { data: 'Period To', title: 'Period To' },
                { data: 'Payment Method', title: 'Payment Method' },
                { data: 'Payment Amount', title: 'Payment Amount' },
                { data: 'Payment Date', title: 'Payment Date' }
            ],
            language: {
                search: "Filter records:",  // Customize search label
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                paginate: {
                    previous: "Previous",
                    next: "Next"
                }
            }
        });

        // Load dataset when the button is clicked (refresh or reload the DataTable)
        $('#load-dataset').on('click', function() {
            $('#status-message').text("Loading dataset...");
            table.ajax.reload(function() {
                $('#status-message').text("Dataset loaded successfully.");
            });
        });
    } else {
        $('#status-message').text("No dataset to load.");
    }
});
