let map;
const KENYA_BOUNDS = {
  north: 5.5,
  south: -5,
  west: 33.8,
  east: 42,
};

const NAIROBI = { lat: -1.2921, lng: 36.8219 };

async function initMap() {

  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  map = new Map(document.getElementById("map"), {
    center: NAIROBI,
    restriction: {
      latLngBounds: KENYA_BOUNDS,
      strictBounds: false,
    },
    zoom: 10,
    mapId: "AIzaSyB7DIN729aJWX85qpD3Fl5S_FDNarHMSSY",
  });

const searchInput = document.getElementById('address');
const autocomplete = new google.maps.places.Autocomplete(searchInput, {
  componentRestrictions: {country: 'ke'}
});

autocomplete.addListener('place_changed', () => {
  const place = autocomplete.getPlace();
  if(!place.geometry){
    console.log('No place data available');
    return;
  }

  const location = place.geometry.location;
  
  const latitude = document.getElementById('latitude');
  const longitude = document.getElementById('longitude');

  latitude.value = location.lat();
  console.log(location.lat())
  longitude.value = location.lng();
  console.log(location.lng())

  map.setCenter(location);

  const marker = new AdvancedMarkerElement({
    map: map, 
    gmpDraggable: true,
    position: location,
  });

  const infoWindow = new InfoWindow();

  infoWindow.setContent('You may drag the marker to a precise location');
  infoWindow.open(marker.map, marker);

  setTimeout(() => {
    infoWindow.close();
  }, 3000);


  marker.addListener('dragend', () => {
    const newPosition = new google.maps.LatLng(marker.position);
    console.log(newPosition);

    latitude.value = newPosition.lat();
    console.log(newPosition.lat());
    longitude.value = newPosition.lng();
    console.log(newPosition.lng());


    infoWindow.close();
    infoWindow.setContent(`Pin dropped at ${newPosition.lat()}, ${newPosition.lng()}`);
    infoWindow.open(marker.map, marker);
  });  

});

}


document.addEventListener('DOMContentLoaded', function(){ 

  let clearBtn = document.querySelector('#clear');
  if(clearBtn){
    clearBtn.addEventListener('click', (event) =>{
      event.preventDefault();
      document.querySelector('#address').value = "";
  
    });
  }
  
  let likebtns = document.querySelectorAll('.likebtn');
  likebtns.forEach(likebtn =>{
    
    let id = likebtn.getAttribute('id');
    fetch(`likes/${id}`)
    .then(res => res.json())
    .then(info => {
      if(info.user_liked){
        likebtn.style.color = 'red';
      }
      else{
        likebtn.style.color = 'white';
      }
    })
    .catch(err => {
      console.error(err);
    });

    likebtn.addEventListener('click', function(event){
      event.preventDefault();
      if(this.style.color !== 'red'){

        this.style.color = 'red';
        const id = this.getAttribute('id');
        
        fetch(`likes/${id}`,{
          method: 'POST',
          body: JSON.stringify({
            likes: 1
          })
        }).then(() => {
          fetch(`likes/${id}`)
          .then(res => res.json())
          .then(comment => {

            this.parentElement.querySelector('.like_count').innerHTML = comment.likes;

          })
          .catch(err => {
            console.error(err);
          });

        }).catch(err => {
          console.err(err);
        });
      }
      else{
        let comment_id = this.getAttribute('id');
        fetch(`likes/${comment_id}`, {
          method: 'POST',
          body: JSON.stringify({
            likes: 0
          })
        }).then(() => {
          fetch(`likes/${id}`)
          .then(res => res.json())
          .then(comment => {
            this.parentElement.querySelector('.like_count').innerHTML = comment.likes;
            this.style.color = 'white';
          }).catch(err => {
            console.error(err);
          });
        }).catch(err => {
          console.error(err);
        });
      }
    });
  })

});

window.initMap = initMap;


