
class PageFooter extends HTMLElement {

  constructor() {
    super();
    //this._shadow = this.attachShadow({mode: 'open'});
  }

  connectedCallback() {
    this._updateRendering();
  }

  _updateRendering() {

    var footerHtml = `<p>Tayport Community Website<br /><br />Supported by Tayport Community Council [April 2003 – present]<br /></p>`;

    var footerScript = `
<!-- google analytics -->
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-274412-4', 'auto');
  ga('send', 'pageview');

</script>
`;

    //this.shadowRoot.innerHTML = footerHtml + footerScript;
    this.innerHTML = footerHtml + footerScript;

  }

}

customElements.define('page-footer', PageFooter);

