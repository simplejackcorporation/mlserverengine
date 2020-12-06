var width = 666;
var height = 0;

var streaming = false;

var video = null;
var canvas = null;
var photo = null;
var startbutton = null;
var socket = null;

function startup() {

  socket = io.connect('http://localhost:8009')

//  socket.on('after connect', function (socket) {
//    console.log("after connection")
//  })

  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  photo = document.getElementById('photo');
  startbutton = document.getElementById('startbutton');

  navigator.mediaDevices.getUserMedia({video: true, audio: false})
  .then(function(stream) {
    video.srcObject = stream;
    video.play();
  })
  .catch(function(err) {
    console.log("An error occurred: " + err);
  });

  video.addEventListener('canplay', function(ev){
    if (!streaming) {
      height = video.videoHeight / (video.videoWidth/width);

      // Firefox currently has a bug where the height can't be read from
      // the video, so we will make assumptions if this happens.

      if (isNaN(height)) {
        height = width / (4/3);
      }

      video.setAttribute('width', width);
      video.setAttribute('height', height);
      canvas.setAttribute('width', width);
      canvas.setAttribute('height', height);
      streaming = true;


      loopFunction(1000, sendPicture); // call every 1 sec
    }
  }, false);
}


function loopFunction(delay, callback){
    var loop = function(){
        callback();
        setTimeout(loop, delay);
    }; loop();
};


function sendPicture() {
//    console.log("sendPicture")

    var data = canvas.toDataURL('image/png');

//    socket.send({"data":"vova"});

//  var context = canvas.getContext('2d');
//  if (width && height) {
//    canvas.width = width;
//    canvas.height = height;
//    context.drawImage(video, 0, 0, width, height);


//    socket.send({"data":data});
//  }
}


window.addEventListener('load', startup, false);


//
//function takepicture() {
//  var context = canvas.getContext('2d');
//  if (width && height) {
//    canvas.width = width;
//    canvas.height = height;
//    context.drawImage(video, 0, 0, width, height);
//
//    var data = canvas.toDataURL('image/png');
//    photo.setAttribute('src', data);
//  }
//}


