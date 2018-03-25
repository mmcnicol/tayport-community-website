
class PageHeader extends HTMLElement {

  constructor() {
    super();
    //this._shadow = this.attachShadow({mode: 'open'});
  }

  connectedCallback() {
    this._updateRendering();
  }

  _updateRendering() {

    //this.shadowRoot.innerHTML = `<h1>Tayport Community Website</h1><h2>`+this.get('sub-title')+`</h2>`;
    this.innerHTML = `<h1>Tayport Community Website</h1><h2>`+this._get('sub-title')+`</h2>`;

  }

  _get(name) {
    if(this.hasAttribute(name)) {
      return this.getAttribute(name);
    } else {
      return null;
    }
  }

}

customElements.define('page-header', PageHeader);

