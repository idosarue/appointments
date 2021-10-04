
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
  if (button.innerText == 'walk'){
    myMove()
    manButton.classList.toggle('walk')
    button.innerText = 'stop'
  }else{
    manButton.classList.toggle('walk')

  clearInterval(id);

    button.innerText = 'walk'

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


