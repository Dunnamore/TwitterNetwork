const API_KEY = `AIzaSyBu9BR7BEYs6z8xuWnQQ1RurDpPKwugiLA`;

const getCoordinates = async (places) => {
  let coordinates = [];
  for (entry of places) {
    const place = entry[0];

    const { lat, lng } = await getLatLng(place);

    coordinates.push([lat, lng]);
  }
  return coordinates;
};

async function getLatLng(address) {
  // await response of fetch call
  let response = await fetch(
    `https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${API_KEY}`
  );
  // only proceed once promise is resolved
  let data = await response.json();
  // only proceed once second promise is resolved
  return data.results[0].geometry.location;
}

async function initMap() {
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 3,
    center: new google.maps.LatLng(0, 0),
  });

  for (let entry of places) {
    const place = entry[0];
    const votes = entry[1];

    const co = await getLatLng(place);

    let marker = new google.maps.Marker({
      position: co,
      map: map,
    });

    let infowindow = new google.maps.InfoWindow({
      content: `<font color="green">${place}, ${votes}</font> `,
    });
    google.maps.event.addListener(marker, 'click', () => infowindow.open(map, marker));
  }
}
