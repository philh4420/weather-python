// document.addEventListener("DOMContentLoaded", function () {
//   if (navigator.geolocation) {
//     navigator.geolocation.getCurrentPosition(showPosition, showError);
//   } else {
//     alert("Geolocation is not supported by this browser.");
//   }
// });

// function showPosition(position) {
//   fetch(`/weather?lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
//     .then(response => {
//       if (!response.ok) {
//         throw new Error(`HTTP error! Status: ${response.status}`);
//       }
//       return response.json();
//     })
//     .then(data => {
//       if (data.error) {
//         alert(`Error: ${data.error}`);
//       } else {
//         document.getElementById('weather-data').innerHTML = data.html;
//       }
//     })
//     .catch(error => {
//       console.error('There was a problem with the fetch operation:', error);
//       alert("Failed to fetch weather data.");
//     });
// }

// function showError(error) {
//   switch (error.code) {
//     case error.PERMISSION_DENIED:
//       alert("User denied the request for Geolocation.");
//       break;
//     case error.POSITION_UNAVAILABLE:
//       alert("Location information is unavailable.");
//       break;
//     case error.TIMEOUT:
//       alert("The request to get user location timed out.");
//       break;
//     case error.UNKNOWN_ERROR:
//       alert("An unknown error occurred.");
//       break;
//   }
// }
