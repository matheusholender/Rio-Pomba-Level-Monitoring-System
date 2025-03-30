// resize.js
function updateReguaSize() {
    var reguaGroup = document.getElementById('regua-group');
    var svgWidth = reguaGroup.parentElement.clientWidth;
    var svgHeight = reguaGroup.parentElement.clientHeight;
    var scaleX = svgWidth / 1366; // 1366 is the original width of the SVG
    var scaleY = svgHeight / 768; // 768 is the original height of the SVG
    var scale = Math.min(scaleX, scaleY);
    reguaGroup.setAttribute('transform', 'scale(' + scale + ')');
  }
  window.addEventListener('resize', updateReguaSize);
  updateReguaSize(); // Initial call to set the initial size
  