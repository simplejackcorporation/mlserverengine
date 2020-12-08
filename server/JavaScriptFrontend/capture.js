var width = 666;
var height = 0;

var streaming = false;

var video = null;
var canvas = null;
var photo = null;
var startbutton = null;
var socket = null;

var skeleton = [[15, 13], [13, 11], [16, 14], [14, 12], [11, 12], [5, 11], [6, 12], [5, 6], [5, 7],
                [6, 8], [7, 9], [8, 10], [1, 2], [0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [0, 5], [0, 6]]

var dumped_xs
var dumped_ys
var dumped_confs

function startup() {
//  import { hello } from './module.js';

//  socket = io.connect('http://localhost:8009')
  var url = 'http://localhost:8009'
  socket = io(url, {
  transportOptions: {
    polling: {
      extraHeaders: {
        'Access-Control-Allow-Origin': '*',
//        'Origin': url
      }
    }
  }
});

  socket.on('video received', function (socket) {
    console.log("video received HERE")
  })

  socket.on('after connect', function (socket) {
    console.log("VOVA HERE")
    loopFunction(150, sendPicture); // call every 1 sec
  })

   socket.on('model did predict', function (socket) {
    console.log("prediction received")
    console.log(socket)

    dumped_xs = socket["dumped_xs"]
    dumped_ys = socket["dumped_ys"]
    dumped_confs = socket["dumped_confs"]
  })

  socket.on('Video received', function (socket) {
    console.log('VIDEO received')
  })

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
  var context = canvas.getContext('2d');
  if (width && height) {
    canvas.width = width;
    canvas.height = height;
    context.drawImage(video, 0, 0, width, height);

    var data = canvas.toDataURL('image/png');
    console.log("Video send")
    socket.emit('send video', {"data":data});
    if (dumped_xs) {
        drawPoints(dumped_xs, dumped_ys, dumped_confs)
    }
  }
}

function drawPoints(xs, ys, confs) {

    // format is (Y, X) (Why ?)
    var xs = getNumberListFromString(xs)
    var ys = getNumberListFromString(ys)
    var confs = getNumberListFromString(confs)

    var context = canvas.getContext('2d');
    var ctx = canvas.getContext('2d');

   for (var i = 0; i<=xs.length; i++) {
    x = xs[i]
    y = ys[i]
    c = confs[i]

    ctx.beginPath();

    ctx.arc(y, x, 20, 0, 2 * Math.PI, false);
    ctx.stroke();
   }

   for (var i = 0; i < skeleton.length - 1; i++) {
    var item = skeleton[i]
    console.log(skeleton[i])
    console.log('\n\n')

    var first_point_index = item[0]
    var second_point_index = item[1]

    var fp_x = xs[first_point_index]
    var fp_y = ys[first_point_index]

    var sp_x = xs[second_point_index]
    var sp_y = ys[second_point_index]
//
    ctx.beginPath();
	ctx.moveTo(fp_y, fp_x);
	ctx.lineTo(sp_y, sp_x, 6);

	ctx.strokeStyle = '#000000';
	ctx.stroke()
   }

}

function getNumberListFromString(numpystr) {
   array = numpystr.match(/\d+(?:\.\d+)?/g).map(Number)

   return array

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


