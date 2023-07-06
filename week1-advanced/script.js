// Get the menu and dropdown elements
const menu = document.querySelector('.menu');
const dropdown = document.querySelector('.dropdown');
dropdown.style.display === 'none'
// Toggle the dropdown on menu click
menu.addEventListener('click', function () {
  dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
});

// Hide the dropdown when clicking outside of it
document.addEventListener('click', function (event) {
  const targetElement = event.target.parentNode.className;
  console.log("dropdown.style.display = " + dropdown.style.display)

  console.log("targetElement = ", targetElement);
  if (dropdown.style.display === 'block') {
    if (!(targetElement == 'dropdown'
      || targetElement == 'right'
      || targetElement == 'item'
      || targetElement == 'menu')
    ) {
      dropdown.style.display = 'none';
      console.log("hide dropdown");
    }
  }

});