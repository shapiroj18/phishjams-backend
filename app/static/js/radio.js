var songs = [
    {
    "name": "Shafty",
    "artist": "Phish",
    "url": "https://phish.in/audio/000/018/032/18032.mp3",
    "cover_art_url": "static/img/livephish_logos/1998-04-05.jpg" 
    }
]


Amplitude.init({
    "bindings": {
      37: 'prev',
      39: 'next',
      32: 'play_pause'
    },


    "songs": songs

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