var elem = document.getElementById("walk-container");
var button = document.getElementById('click');
var handContainer = document.getElementById('hand-container');
button.addEventListener('click', startStop);
var currentPosition;
var carButton = document.getElementById('truck')
var videoCon = document.getElementById('con')

$(document).ready(function(){
    $('#con').css('width', $('#myVideoCon').css('width'))
    $('#hand-container').css('width', $('#myVideoCon').css('width'))
});



function startStop(){
  console.log(button.innerText)
  if (button.innerText == 'go'|| button.innerText == 'סע'){
    myMove()
    if(button.innerText == 'go'){
      $('#hand').hide()
      button.innerText = 'stop'
    }else if (button.innerText == 'סע'){
      $('#hand').hide()
      button.innerText = 'עצור'
    }
    carButton.classList.toggle('go')
  }else{
    carButton.classList.toggle('go')
    clearInterval(id);
    if(button.innerText == 'stop'){
      button.innerText = 'go'
    }else if (button.innerText == 'arrêter'){
      button.innerText = 'marche'
    }else if (button.innerText == 'עצור'){
      button.innerText = 'סע'
    }

  }
}

function myMove() {
  var screen = $(window).width()
  console.log(screen)

  var pos = 0;
  currentPosition = elem.style.left
  currentPosition = currentPosition.replace(/\D/g,'');
  console.log(currentPosition)
  id = setInterval(frame, 10);
  carButton.style.transform = "scaleX(1)";
  function frame() {
    if (pos > videoCon.style.width.replace(/\D/g,'') - 100) {
      clearInterval(id);
      myMoveLeft()
    }else {
      currentPosition++;
      console.log(currentPosition)
      pos++
      elem.style.left = pos + 'px';
    }
}
}

function myMoveLeft() {
  var pos = 0;
  currentPosition = elem.style.left
  currentPosition = currentPosition.replace(/\D/g,'');
  id = setInterval(frame, 10);
  carButton.style.transform = "scaleX(-1)";
  function frame() {
    if (currentPosition <= 1) {
      clearInterval(id);
      myMove()
    }else {
      currentPosition--;
      console.log(currentPosition)
      pos--
      elem.style.left = currentPosition + 'px';
    }

    }
}


var video = document.getElementById("myVideo");
var stopButton = document.getElementById("stopButton");
stopButton.addEventListener('click', play)



function stopVideo(){
    $("#stopButton").toggleClass("btn-success")
    $("#stopButton").toggleClass("btn-danger")
    $("#myVideoCon").toggleClass("show");
}
function startVideo(){
  $("#myVideoCon").toggleClass("show");
  $("#stopButton").toggleClass("btn-success")
  $("#stopButton").toggleClass("btn-danger")
}

function play(){
  if (stopButton.className == 'btn btn-danger'){
    stopVideo()
  }else{
    startVideo()
  }
}