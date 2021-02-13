// function getCoverArtURL(date) {
//   var basepath = "static/img/livephish_logos/"
//   var img_url = basepath + date + ".jpg"

//   return img_url

  // return new Promise(resolve => {
  //   fetch(img_url).then(res => {
  //     if (res.status = 200) {
  //       resolve(img_url);
  //     } else {
  //       resolve(default_img_url);
  //     };
  //   });
  // })
  // return await fetch(img_url, { method: 'HEAD' })
  //   .then(res => {
  //       if (res.ok) {
  //           return img_url;
  //       } else {
  //           return default_img_url;
  //       }
  //   }).catch(err => console.log('Error:', err));
// }


const songs = [
    {
    "name": "Shafty",
    "artist": "Phish",
    "url": "https://phish.in/audio/000/018/032/18032.mp3",
    "cover_art_url": "static/img/livephish_logos/1999-12-31.jpg"
    },
    {
      "name": "Harry Hood",
      "artist": "Phish",
      "url": "https://phish.in/audio/000/020/602/20602.mp3",
      "cover_art_url": "static/img/livephish_logos/1999-12-31.jpg"
      }
]

// async function getSongs() {
//   let url = '/get_song_info';
//   let resp = await fetch(url)
//   if (resp.ok) {
//     let json = await resp.json();
//     console.log(json);
//     return {
//       "name": json.name,
//       "artist": json.artist,
//       "url": json.url,
//       "cover_art_url": json.cover_art_url,
//     };
//   } else {
//     alert("HTTP-Error: " + response.status);
//   }
// }

// getSongs().resolve('Success')


// console.log(thesesongs)

// const getsongs = async () => {
//   const json = await fetch('/get_song_info').then(response => response.json());
//   console.log(json);
// }

const obj_name = fetch("/get_song_info")
  .then((response) => response.json())
  .then((object) => {
    return object
  });

const printObj = () => {
  obj_name.then((a) => {
    return a;
  });
};

// printObj();



// async function getsong_info(){ return await getSongs()}

async function create_amplitude() {

  const songs_async = await printObj()

  Amplitude.init({
    "bindings": {
      37: 'prev',
      39: 'next',
      32: 'play_pause'
    },

    "songs": songs_async
  });

  window.onkeydown = function(e) {
      return !(e.keyCode == 32);
  };

  /*
    Handles a click on the song played progress bar.
  */
  document.getElementById('song-played-progress').addEventListener('click', function( e ){
    var offset = this.getBoundingClientRect();
    var x = e.pageX - offset.left;

    Amplitude.setSongPlayedPercentage( ( parseFloat( x ) / parseFloat( this.offsetWidth) ) * 100 );
  });
}

create_amplitude()