window._$recorder = { };

//capture clicks to get element selected attributes
window._$recorder.dump_attributes = function(elm) {
  var result = [];
  for(var i = 0;i < elm.attributes.length;i++) {
    attribute = elm.attributes[i];
    result.push([attribute.name,attribute.value]);
  }
  return result;
};

window._$recorder.click_events = [];
window._$recorder.last_clicked_elm = null;
//old element = "element","border-style","border-width","border-color"

window._$recorder.highlight_element = function(elm) {
    var keys = ["border-style","border-style","border-color"];
    //restore old element
    if(window._$recorder.last_clicked_elm) {
        var oldElm = window._$recorder.last_clicked_elm["element"];
        keys.forEach(function(key) {
            oldElm.style[key] = window._$recorder.last_clicked_elm[key];
        });}
    
    //save element properties
    var backupElm = {};
    backupElm["element"] = elm;
    keys.forEach(function(key) {
        backupElm[key] = elm.style[key];
    });
    window._$recorder.last_clicked_elm = backupElm;

    //change element
    elm.style["border-style"] = "dashed";
    elm.style["border-width"] = "2px";
    elm.style["border-color"] = "red";

    return true;
};

window._$recorder.dump_element = function(event) {
    var result = [];
    var currentElement = event.target;
    window._$recorder.highlight_element(currentElement);
    console.log(currentElement);
    do {
        result.push([
            ["tag", currentElement.tagName.toLowerCase()],
            ["attributes",window._$recorder.dump_attributes(currentElement)]
        ]);
        currentElement = currentElement.parentElement;
    } while(currentElement.tagName.toLowerCase() != "body");
    window._$recorder.click_events.push(result);
    return result;
};

window._$recorder.highlighted_elements = [];

window._$recorder.highlight_css_selected =  function(cssSelector) {
    window._$recorder.unhighlight_css_selected();
    var elms = document.querySelectorAll(cssSelector);
    elms = Array.prototype.slice.call(elms);
    var highlightedElms = elms.map(function(elm) {
        var keys = ["border-style","border-style","border-color"];
        var backupElm = {};
        backupElm["element"] = elm;
        keys.forEach(function(key) {
            backupElm[key] = elm.style[key];
        });
        elm.style["border-style"] = "dashed";
        elm.style["border-width"] = "2px";
        elm.style["border-color"] = "red";
        return backupElm;
    });
    window._$recorder.highlighted_elements = highlightedElms;
};

window._$recorder.unhighlight_css_selected = function() {
    var oldElms = window._$recorder.highlighted_elements;
    oldElms.forEach(function(oldElm) {
        var elm = oldElm["element"];
        var keys = ["border-style","border-style","border-color"];
        keys.forEach(function(key) {
            elm.style[key] = oldElm[key];
        });
    });
    window._$recorder.highlighted_elements = [];
};

window._$recorder.keydownListner = function(event) {
    //event.key does not work on chrome, use keyCode
    //91 == Windows Key or "OS"
    //console.log("keydownListner",event.key,event.keyCode,event.target)
    if(event.keyCode == 91) {
        window.addEventListener("click",window._$recorder.dump_element,false);
    }};

window._$recorder.keyupListner = function(event) {
    //console.log("keyupListner",event.key,event.keyCode,event.target)
    if(event.keyCode == 91) {
        window.removeEventListener("click",window._$recorder.dump_element,false);
    }};

window._$recorder.start = function() {
    window.addEventListener("keydown",
                            window._$recorder.keydownListner,
                            false);
    window.addEventListener(
        "keyup",
        window._$recorder.keyupListner,
        false);    
};

window._$recorder.stop = function() {
    window.removeEventListener("keydown",
                            window._$recorder.keydownListner,
                            false);
    window.removeEventListener(
        "keyup",
        window._$recorder.keyupListner,
        false);    
};

//http://stackoverflow.com/questions/15505225/inject-css-stylesheet-as-string-using-javascript
//http://davidwalsh.name/add-rules-stylesheets
window._$recorder.add_style_sheet = function() {
    var node = document.createElement('style');
    document.body.appendChild(node);
    window._$recorder.edit_style_string = function(str) {
        node.innerHTML = str;
    }
};

