var a;
function pass(){
    if(a==1){
        document.getElementById('password').type='password';
        document.getElementById('pass-icon').src='fa-regular fa-eye';
        a=0;
    }
    else{
        document.getElementById('password').type='text';
        document.getElementById('pass-icon').src='fa-regular fa-eye';
        a=1;
    }
}
var i = 0;
var txt = 'Hello Everyone'; /* The text */
var speed = 50; /* The speed/duration of the effect in milliseconds */

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("typewrite").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}