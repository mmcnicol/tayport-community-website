
var registerElementSupported = 'registerElement' in document;

if(!registerElementSupported) {
  var div = document.createElement('div');
  div.innerHTML = "this page uses web components which are only currently supported by modern browsers.";
  document.body.appendChild(outOfDocument);
}


/*
var webComponentsSupported = ('registerElement' in document
    && 'import' in document.createElement('link')
    && 'content' in document.createElement('template'));
*/

