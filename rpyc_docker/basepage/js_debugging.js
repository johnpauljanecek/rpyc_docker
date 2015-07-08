//hook ajax
var captureAjax = null;
//captureAjax.responseText
(function() {
    var origOpen = XMLHttpRequest.prototype.open;
    var origSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function(method,url) {
        captureAjax = this;
        console.log("XMLHttpRequest.prototype.open",
                    this,method,url);        
        origOpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function(method,url) {
        captureAjax = this;
        console.log("XMLHttpRequest.prototype.send",
                    this,arguments);        
        origSend.apply(this, arguments);
    };
    
})();

window._$recorder = { };

//capture clicks to get element selected attributes
window._$recorder.dump_attributes = function(elm) {
  var result = [];
  for(var i = 0;i < elm.attributes.length;i++) {
    attribute = elm.attributes[i];
    result.push([attribute.name,attribute.value]);
  }
  return result;
}

window._$recorder.click_events = [];

window._$recorder.dump_element function(event) {
    var result = [];
    var currentElement = event.target;
    console.log(currentElement);
    do {
        result.push([
            ["tag" : currentElement.tagName.toLowerCase()],
            ["attributes" : dump_attributes(currentElement)]
        ]);
    } (currentElement.tagName.toLowerCase() != "body");
    window._$recorder.click_events.push(dump);
    return dump;
};

window._$recorder.keydownListner(event) {
    console.log("keydownListner")
    if(event.key == "OS") {
        window.addEventListener("click",window._$recorder.dump_element,false);
    }};

window._$recorder.keyupListner(event) {
    console.log("keyupListner")
    if(event.key == "OS") {
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
