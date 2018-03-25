
class PhotoGallery extends HTMLElement {

  constructor() {
    super();
    //this._shadow = this.attachShadow({mode: 'open'});
  }

  connectedCallback() {
    this._updateRendering();
  }

  _updateRendering() {

    var navHtml = `<p>`;
    if(this._get('prev')!='') {
      navHtml = navHtml + `<a href="../`+this._get('prev')+`">prev</a>`;
    }
    if(this._get('next')!='') {
      navHtml = navHtml + ` <a href="../`+this._get('next')+`">next</a>`;
    }
    navHtml = navHtml + `</p>`;

    var photoHtml = `<p><img src="../../media/`+this._get('filename')+`" width="`+this._get('width')+`" height="`+this._get('height')+`" /></p>`;

    //this.shadowRoot.innerHTML = navHtml + photoHtml;
    this.innerHTML = navHtml + photoHtml;
  }

  _get(name) {
    if(this.hasAttribute(name)) {
      return this.getAttribute(name);
    } else {
      return null;
    }
  }

}

customElements.define('photo-gallery', PhotoGallery);

