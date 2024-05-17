document.addEventListener("DOMContentLoaded", function () {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
});

function showPosition(position) {
  fetch(`/weather?lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
    .then(response => response.json())
    .then(data => {
      document.getElementById('weather-data').innerHTML = data.html;
    });
}

function showError(error) {
  alert("Geolocation is not enabled or not available.");
}
