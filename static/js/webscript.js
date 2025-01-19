document.addEventListener('DOMContentLoaded', () => {
  // Select all buttons with the class 'explore-btn'
  const exploreButtons = document.querySelectorAll('.explore-btn');

  // Add a click event listener to each button
  exploreButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      event.preventDefault(); // Prevent default link behavior

      // Get the product title from the closest product card
      const productTitle = event.target.closest('.product-card').querySelector('h3').textContent;

      // Determine which page to redirect to based on the product title
      let redirectPage = '';
      if (productTitle === 'Ferro Alloys') {
        redirectPage = 'ferroalloys.html';
      } else if (productTitle === 'Minor Metals') {
        redirectPage = 'minormetals.html';
      }

      // Redirect to the appropriate page
      if (redirectPage) {
        window.location.href = redirectPage; // Directly redirect without alert
      }
    });
  });
});
document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');

  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
  });

  // Add event listener to document to close popup menu when clicking outside
  document.addEventListener('click', (event) => {
    if (!navLinks.contains(event.target) && !hamburger.contains(event.target)) {
      navLinks.classList.remove('active');
    }
  });
});


























































 




  














