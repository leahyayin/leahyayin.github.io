// ==== code for w3 assignment ====
async function fetchData(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    console.log(data.result.results)
    return data.result.results;
  } catch (error) {
    console.error("Error fetching data:", error);
    return [];
  }
}
// Function to create and append an main bar promotion div
function createBarElement(attraction) {
  let barDiv = document.createElement("div");
  barDiv.className = "promotion";

  let img = document.createElement("img");
  img.src = "https://" + attraction.file.split("https://")[1];
  img.alt = attraction.stitle;
  barDiv.appendChild(img);

  const title = document.createTextNode(attraction.stitle);
  barDiv.appendChild(title);
  return barDiv;
}

// Function to create and append Gallery element
function createGalleryElement(attraction) {
  let productDiv = document.createElement("div");
  productDiv.className = "product";

  let cardDiv = document.createElement("div");
  cardDiv.className = "image-card";
  productDiv.appendChild(cardDiv);

  let img = document.createElement("img");
  img.className = "spot";
  img.src = "https://" + attraction.file.split("https://")[1];
  img.alt = attraction.stitle;
  cardDiv.appendChild(img);

  let titleDiv = document.createElement("div");
  titleDiv.className = "title-inner";
  titleDiv.textContent = attraction.stitle;
  productDiv.appendChild(titleDiv);

  return productDiv;
}

// Function to display attractions
let attractions = undefined;
async function displayAttractions(curImgNum, displayImgNum) {
  if (!attractions) {
    const attractionsUrl = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json";
    attractions = await fetchData(attractionsUrl);
  } else {
    console.log("attractions already existed")
  }
  const mainBarDiv = document.querySelector(".main-bar");
  const galleryDiv = document.querySelector(".gallery");

  if (attractions.length > 0) {
    // Display the first 3 attractions on the bar
    if (curImgNum === 0) {
      for (let i = 0; i < 3; i++) {
        const attraction = attractions[i];
        const attractionElement = createBarElement(attraction);
        mainBarDiv.appendChild(attractionElement);
        updateCurImgNum(i + 1);
      }
    }
    // Display the next 12 attractions below the top 3
    for (let j = getImgIndex(); j < displayImgNum && j < attractions.length; j++) {
      const attraction = attractions[j];
      const attractionElement = createGalleryElement(attraction);
      galleryDiv.appendChild(attractionElement);
      if (updateCurImgNum(j + 1) == attractions.length) {
        document.querySelector(".loadBtn").textContent = "No more atractions";
        document.querySelector(".loadBtn").disabled = true;
      }
    }
  } else {
    galleryDiv.textContent = "No attractions found";
  }
}

// Task 4: Call the function to display attractions on page load
let curImgNum = 0; let defaultImgNum = 12;
function updateCurImgNum(newImgNum) {
  curImgNum = newImgNum;
}
function getImgIndex() {
  return curImgNum;
}

displayAttractions(curImgNum, defaultImgNum);

// handle loading
document.querySelector(".main").addEventListener(
  'load', () => {
    console.log('page is fully loaded');
    document.querySelector(".loading").style.display = "none";
    document.querySelector(".main").style.display = "flex";

  }, "error", () => {
    console.log('Failed to load image');
    document.querySelector(".main").textContent = "Failed to load image.";
  });

// handle button click to load more
function imgAddCount(addNum) {
  return curImgNum += addNum
};

document.addEventListener('DOMContentLoaded', () => {
  const loadBtn = document.querySelector(".loadBtn");
  loadBtn.addEventListener('click', () => 
    displayAttractions(curImgNum, imgAddCount(12))
  );
});

// ==== code for w1 assignment ====
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