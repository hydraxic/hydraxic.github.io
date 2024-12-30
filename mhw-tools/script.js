document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded');

    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    // hide all tab contents except the first one
    tabButtons.forEach((button, index) => {
        if (index === 0) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
    
    tabContents.forEach((content, index) => {
        if (index === 0) {
            content.style.display = 'block';
        } else {
            content.style.display = 'none';
        }
    });

    tabButtons.forEach((button) => {
        button.addEventListener('click', () => {
            // remove active class from all buttons and assign to clicked button
            tabButtons.forEach((button) => {
                button.classList.remove('active');
            });

            // hide tab contents
            tabContents.forEach((content) => {
                content.style.display = 'none';
            });

            // add active tab to clicked button and show content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).style.display = 'block';
        });
    });
});
