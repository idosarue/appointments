
$(document).ready(function(){
    $(".confirm_delete").click(function(){
        return confirm('Are you sure you want to cancel this appointment?');
    });
});

$(document).ready(function(){
    $(".comment-confirm-delete").click(function(){
        return confirm('Are you sure you want to delete this comment?');
    });
});




var id = null;
var elem = document.getElementById("walk-container");
var button = document.getElementById('click');
button.addEventListener('click', startStop);
var currentPosition;
var manButton = document.getElementById('man')

function startStop(){
  if (button.innerText == 'walk' || button.innerText == 'marche' || button.innerText == 'לך'){
    myMove()
    if(button.innerText == 'walk'){
      button.innerText = 'stop'
    }else if (button.innerText == 'marche'){
      button.innerText = 'arrêter'
    }else if (button.innerText == 'לך'){
      button.innerText = 'עצור'
    }
    manButton.classList.toggle('walk')
  }else{
    manButton.classList.toggle('walk')
    clearInterval(id);
    if(button.innerText == 'stop'){
      button.innerText = 'walk'
    }else if (button.innerText == 'arrêter'){
      button.innerText = 'marche'
    }else if (button.innerText == 'עצור'){
      button.innerText = 'לך'
    }

  }
}

function myMove() {
  var screen = $(window).width()
  console.log(screen)

  var pos = 0;
  currentPosition = elem.style.left
  currentPosition = currentPosition.replace(/\D/g,'');
  id = setInterval(frame, 10);
  manButton.style.transform = "scaleX(1)";

  function frame() {
    if (pos > screen - 200) {
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
  manButton.style.transform = "scaleX(-1)";
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

