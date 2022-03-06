function changeSliderStatus(circleIndex) {
  // Change active circle
  document.querySelectorAll('.circle').forEach(
    (circle) => {
      if (circle.className.includes('--Active')) {
        if (circle.title != circleIndex) {
          circle.className = 'circle';
        }
      } else if (circle.title === circleIndex) {
        circle.className += ' --Active';
      }
    }
  );
  
  // Swap current image
  document.getElementsByClassName('sliderImageItem')[0].src = "./img/slide" + circleIndex + ".png";
}
