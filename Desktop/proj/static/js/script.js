document.addEventListener('DOMContentLoaded', function() {
    const toggleSidebarButton = document.getElementById('toggleSidebar');
    const closeSidebarButton = document.getElementById('closeSidebar');
    const sidebar = document.getElementById('sidebar');
    const profileImage = document.getElementById('profileImage');
    const profileDropdown = document.getElementById('profileDropdown');
    const tabLinks = document.querySelectorAll('.nav-link');
    const tabContents = document.querySelectorAll('.tab-pane');
  

    // Toggle sidebar visibility
    toggleSidebarButton.addEventListener('click', function() {
        sidebar.style.width = '250px';
    });
  
    closeSidebarButton.addEventListener('click', function() {
        sidebar.style.width = '0';
    });
  
    // Profile dropdown functionality
    profileImage.addEventListener('mouseenter', function() {
        profileDropdown.style.display = 'block';
    });
  
    profileImage.addEventListener('mouseleave', function() {
        setTimeout(function() {
            profileDropdown.style.display = 'none';
        }, 200);
    });
  
    profileDropdown.addEventListener('mouseenter', function() {
        profileDropdown.style.display = 'block';
    });
  
    profileDropdown.addEventListener('mouseleave', function() {
        profileDropdown.style.display = 'none';
    });
  
    // Toggle dropdown menu on click
    profileImage.addEventListener('click', () => {
        profileDropdown.style.display = profileDropdown.style.display === 'block' ? 'none' : 'block';
    });
  
    // Close the dropdown if the user clicks outside of it
    window.addEventListener('click', (event) => {
        if (!event.target.matches('#profileImage')) {
            if (profileDropdown.style.display === 'block') {
                profileDropdown.style.display = 'none';
            }
        }
    });
  
    // Tab navigation functionality
    tabLinks.forEach(tabLink => {
        tabLink.addEventListener('click', function(event) {
            event.preventDefault();
  
            // Remove the 'active' class from all tab links and contents
            tabLinks.forEach(link => link.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('show', 'active'));
  
            // Add the 'active' class to the clicked tab link and corresponding content
            tabLink.classList.add('active');
            const targetTab = document.querySelector(tabLink.getAttribute('href'));
            targetTab.classList.add('show', 'active');
        });
    });
  
    // Preview section functionality with jQuery
    $('#upload-form').on('submit', function (e) {
        e.preventDefault();
  
        var formData = new FormData(this);
  
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.preview) {
                    $('#file-content').html(response.preview);
                    $('#preview-section').show();
                } else {
                    $('#file-content').html('<p>Error: Unable to preview the file.</p>');
                }
            },
            error: function () {
                $('#file-content').html('<p>Error: Unable to upload the file.</p>');
            }
        });
    });
  });
  
