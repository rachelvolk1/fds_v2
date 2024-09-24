$(document).ready(function() {
    // Initialize DataTables for each section
    $('#my-tasks-table').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        info: true
    });

    $('#deadline-missed-tasks-table').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        info: true
    });

    $('#task-pool-table').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        info: true
    });

    // Refresh button functionality
    $('#refresh-button').on('click', function() {
        $('#my-tasks-table').DataTable().ajax.reload();
        $('#deadline-missed-tasks-table').DataTable().ajax.reload();
        $('#task-pool-table').DataTable().ajax.reload();
        console.log('Task box refreshed');
    });
});

//dynamic table loading
var myTasksTable = $('#my-tasks-table').DataTable({
    ajax: {
        url: '/api/my-tasks', // Replace with your actual data source
        dataSrc: ''
    },
    columns: [
        { data: 'task_id' },
        { data: 'upload_file_id' },
        { data: 'process_stage' },
        { data: 'activity_name' },
        { data: 'updated_on' },
        { data: 'updated_by' }
    ]
});
