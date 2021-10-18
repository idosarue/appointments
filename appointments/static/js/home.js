
    var mouseDown = 0;
    var mouseUp = 0;
document.body.addEventListener('mousedown', grow)
document.body.addEventListener('mouseup', shrink)
var id = null;

function shrink(){
    var div = document.getElementById('BALL')
    var currentWidth =div.style.width.replace(/\D/g,'');
    var currentHeight = div.style.height.replace(/\D/g,'');
    id = setInterval(frame, 50);
    function frame() {
    ++mouseUp;

        if (currentWidth) {
            currentWidth--;
            currentHeight--;
            div.style.width = currentWidth + 'px';
            div.style.height = currentHeight + 'px';
        }
        else {
            clearInterval(id)
        }
    }

}

function grow(event) {
    var newDiv = document.createElement("div");
    newDiv.id = "BALL"
    newDiv.style.position = "absolute";
    newDiv.style.background = "red";
    newDiv.style.borderRadius = "50%"
    newDiv.style.zIndex = "9999";

    document.body.appendChild(newDiv)
    var currentWidth = newDiv.style.width.replace(/\D/g,'');
    var currentHeight = newDiv.style.height.replace(/\D/g,'');
    newDiv.style.top = event.pageY - 5 + 'px';
    newDiv.style.left = event.pageX - 5 + 'px';
    console.log(currentPosition)
    id = setInterval(frame, 50);
    carButton.style.transform = "scaleX(1)";
    ++mouseDown
    function frame() {
      if (mouseUp) {
        shrink();
      }else {
        currentWidth++;
        currentHeight++
        console.log(currentPosition)
        newDiv.style.width = currentWidth + 'px';
        newDiv.style.height = currentHeight + 'px';
      }
  }
  }


// document.body.onmousedown = function(event) { 
//     ++mouseDown;
//     ++mouseUp
//     console.log(',ousedown')
//     newDiv.style.top = event.pageY - 5 + 'px';
//     newDiv.style.left = event.pageX - 5 + 'px';
//     document.body.appendChild(newDiv)
//     var w = 10;
//     var h = 10;
//     if (mouseDown >= mouseUp){
//         setInterval(function () {
//             w = w + 1;
//             h = h + 1;
//             newDiv.style.width = w + 'px';
//             newDiv.style.height = h + 'px';
//         }, 100);
//     }


//   }

//   newDiv.onmouseup = function(event) {
//     var w = document.getElementById("ball").style.width.replace(/\D/g,'');
//     var h = document.getElementById("ball").style.height.replace(/\D/g,'');
//     ++mouseUp;
//     console.log(mouseDown)
//     console.log('up')
//     alert('up')

//     console.log(w)
//     setInterval(function () {
//         w = w - 1;
//         h = h - 1;
//         document.getElementById("ball").style.width = w + 'px';
//         document.getElementById("ball").style.height = h + 'px';
//     }, 100);
//   }


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