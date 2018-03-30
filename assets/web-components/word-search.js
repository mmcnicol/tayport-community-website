
class WordSearch extends HTMLElement {

  constructor() {
    super();
    //this._shadow = this.attachShadow({mode: 'open'});
    this.debug = false;
  }

  // Specify observed attributes so that attributeChangedCallback will work
  static get observedAttributes() {return ['words', 'size', 'debug']; }

  attributeChangedCallback(name, oldValue, newValue) {
    //console.log('Custom HelloWorld3 element attributes changed.');
    // name will always be "name" due to observedAttributes
    //this._name = newValue;
            switch(name) {
                case 'words':
                    this.words = newValue.split(',');
                    break;
                case 'size':
                    this.size = newValue;
                    break;
                case 'debug':
                    this.debug = true;
                    break;
            }
    this._updateRendering();
  }

  connectedCallback() {
    //this._updateRendering();
  }

  _updateRendering() {

    if(typeof this.words == 'undefined' || typeof this.size == 'undefined' || typeof this.debug == 'undefined') return;

    this.possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    //this.words = ["TAYPORT", "FERRYPORT", "SCOTSCRAIG", "TENTSMUIR", "FIFE", "SCOUTS", "PARISHCHURCH", "AULDKIRK", "FOOTBALL", "HARBOUR", "GOLFCLUB", "CAFE", "CARAVAN", "DOLPHIN", "PLAYGROUP", "COMMUNITYCOUNCIL", "POSTOFFICE", "PRIMARYSCHOOL", "JOBCLUB", "GREGORYHALL", "LIBRARY"];

    this.grid = this._create2DArray(this.size);

    for (y = 0; y < this.size; y++) { 
      for (x = 0; x < this.size; x++) {
        this.grid[y][x]=null;
      }
    }


    // place words
    this.placedWords = new Array;
    for (var i = 0; i < this.words.length; i++) { 
      var word = this.words[i];
      var wordLength = word.length;
      var foundFreeSlot = false;
      var attemptCount = 0;

      while(foundFreeSlot==false && attemptCount<this.size) {
        var textDirection = this._getRandNumBetween(1, 2); // 1=forwards, 2=backwards
        var textOrientation = this._getRandNumBetween(1, 4); // 1=top-bottom, 2=left-right, 3=top-to-bottom-diagonal, 4=bottom-to-top-diagonal
        var x = this._getRandNumBetween(0, this.size-1);
        var y = this._getRandNumBetween(0, this.size-1);
        foundFreeSlot = this._isSlotFee(word, wordLength, x, y, textDirection, textOrientation);
        if(foundFreeSlot) {
          //console.log('found slot!');
          this._setWord(word, wordLength, x, y, textDirection, textOrientation);
          this.placedWords.push(word);
        }
        attemptCount++;
      }
      //console.log('place word attempts='+attemptCount);
    }


    // fill in the grid spaces with random characters
    if(!this.debug) {
      for (y = 0; y < this.size; y++) { 
        for (x = 0; x < this.size; x++) {
          if(this.grid[y][x]==null) {
            this.grid[y][x]=this.possible.charAt(Math.floor(Math.random() * this.possible.length));
          }
        }
      }
    }


    var output="";
    var paragraph1 = document.createElement('p');
    var paragraph2 = document.createElement('p');
    var pre = document.createElement('pre');

    paragraph1.innerText = 'The words to find are:';

    // list words to find
    for (var i = 0; i < this.placedWords.length; i++) { 
      paragraph2.innerText += this.placedWords[i] + '\n';
    }

    // draw grid
    var line = "";
    for (var y = 0; y < this.size; y++) { 
      line = "";
      for (var x = 0; x < this.size; x++) {
        line += ' ' + this._spaceIfNull(this.grid[y][x]);
      }
      //var div = document.createElement('pre');
      //div.innerText = line;
      //document.body.appendChild(div);
      output += line + '\n';
    }

    pre.innerHTML = output;

    this.appendChild(pre);
    this.appendChild(paragraph1);
    this.appendChild(paragraph2);
  }

  _get(name) {
    if(this.hasAttribute(name)) {
      return this.getAttribute(name);
    } else {
      return null;
    }
  }

  _create2DArray(rows) {
    var arr = [];

    for (var i=0;i<rows;i++) {
      arr[i] = [];
    }

    return arr;
  }

  _getRandNumBetween(min, max) {
    return Math.floor(Math.random() * max) + min;
  }

  _reverseArr(input) {
    var ret = new Array;
    for(var i = input.length-1; i >= 0; i--) {
        ret.push(input[i]);
    }
    return ret;
  }

  _isSlotFee(word, wordLength, x, y, textDirection, textOrientation) {

    //console.log('is slot free? "'+word+'" at '+x+','+y+' direction='+textDirection+', orientation='+textOrientation);

    switch(textOrientation) {

      case 1:
        // 1=top-bottom
        if(y + wordLength < this.size) {
          //console.log('there is space in y axis');
          for(var yy=y, charNum=0; charNum<word.length; yy++, charNum++) {
            var currentGridChar = this.grid[yy][x];
            //console.log(currentGridChar);
            if(currentGridChar!=null) {
              //console.log('is not null!');
              if (currentGridChar!=word[charNum]) {
                //console.log(currentGridChar + ' is not '+word[charNum]);
                return false;
              }
            }
          }
          return true;
        }
        break;

      case 2:
        // 2=left-right
        if(x + wordLength < this.size) {
          //console.log('there is space in x axis');
          for(var xx=x, charNum=0; charNum<word.length; xx++, charNum++) {
            var currentGridChar = this.grid[y][xx];
            //console.log(currentGridChar);
            if(currentGridChar!=null) {
              //console.log('is not null!');
              if (currentGridChar!=word[charNum]) {
                //console.log(currentGridChar + ' is not '+word[charNum]);
                return false;
              }
            }
          }
          return true;
        }
        break;

      case 3:
        // 3=top-to-bottom-diagonal
        if(x + wordLength < this.size && y + wordLength < this.size) {
          //console.log('there is space in x axis & y axis');
          for(var yy=y, xx=x, charNum=0; charNum<word.length; yy++, xx++, charNum++) {
            var currentGridChar = this.grid[yy][xx];
            //console.log(currentGridChar);
            if(currentGridChar!=null) {
              //console.log('is not null!');
              if (currentGridChar!=word[charNum]) {
                //console.log(currentGridChar + ' is not '+word[charNum]);
                return false;
              }
            }
          }
          return true;
        }
        break;

      case 4:
        // 4=bottom-to-top-diagonal
        if( (x + wordLength < this.size) && (y - wordLength >= 0) ) {
          //console.log('there is space in x axis & y axis');
          for(var yy=y, xx=x, charNum=0; charNum<word.length; yy--, xx++, charNum++) {
            var currentGridChar = this.grid[yy][xx];
            //console.log(currentGridChar);
            if(currentGridChar!=null) {
              //console.log('is not null!');
              if (currentGridChar!=word[charNum]) {
                //console.log(currentGridChar + ' is not '+word[charNum]);
                return false;
              }
            }
          }
          return true;
        }
        break;

    }

    return false;
  }

  _setWord(word, wordLength, x, y, textDirection, textOrientation) {

    //console.log('setting word "'+word+'" at '+x+','+y+' direction='+textDirection+', orientation='+textOrientation);

    var newWord = word;
    if(textDirection==2) {
      //newWord = word.reverse();
      newWord = this._reverseArr(word);
    }

    switch(textOrientation) {

      case 1:
        // 1=top-bottom
        //console.log('debug');
        for(var yy=y, charNum=0; yy<(y+newWord.length); yy++, charNum++) {
          this.grid[yy][x] = newWord[charNum];
          //console.log(x+','+yy+'='+newWord[charNum]);
        }
        break;

      case 2:
        // 2=left-right
        //console.log('debug');
        for(var xx=x, charNum=0; xx<(x+newWord.length); xx++, charNum++) {
          this.grid[y][xx] = newWord[charNum];
          //console.log(xx+','+y+'='+newWord[charNum]);
        }
        break;

      case 3:
        // 3=top-to-bottom-diagonal
        for(var yy=y, xx=x, charNum=0; xx<(x+newWord.length); yy++, xx++, charNum++) {
          this.grid[yy][xx] = newWord[charNum];
          //console.log(xx+','+yy+'='+newWord[charNum]);
        }
        break;

      case 4:
        // 4=bottom-to-top-diagonal
        for(var yy=y, xx=x, charNum=0; xx<(x+newWord.length); yy--, xx++, charNum++) {
          this.grid[yy][xx] = newWord[charNum];
          //console.log(xx+','+yy+'='+newWord[charNum]);
        }
        break;
    }
  }

  _spaceIfNull(str) {
    if(str==null) return ' ';
    else return str;
  }

}

customElements.define('word-search', WordSearch);

