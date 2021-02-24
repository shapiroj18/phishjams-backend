const jsonResp = fetch("/get_song_info")
  .then((response) => response.json())
  .then((object) => {
    return object
  });

const createAmplitude = () => {
  jsonResp.then((response) => {
    console.log(response);
    Amplitude.init({
      "bindings": {
      37: 'prev',
      39: 'next',
      32: 'play_pause'
    },

    "songs": JSON.parse(response)
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
  });
};

createAmplitude();