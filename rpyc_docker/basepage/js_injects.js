//adds a to body
return function(div_id){
    var div = document.createElement('div');
    document.body.appendChild(div);
    div.setAttribute('id',div_id);
    div.style.left = '32px'; 
    div.style.top = '100px';
    div.style.position="fixed";
    div.style.color="red";
    div.style.position="fixed";
    div.innerHTML = "<ul></ul>";
    return div.document.body.firstElementChild();
}(%s);

//adds a li to the div with text
return function (div_id,text){
    //var div = document.getElementById(div_id);
    var xpath = '//div[@id="'+div_id+'"]/ul';
    var hs = document.evaluate(xpath,document.body,null,XPathResult.ANY_TYPE, null);
    var ul = hs.iterateNext();
    var li = document.createElement('li');
    ul.appendChild(li);
    li.textContent = text;
    return li;
}(%s,%s);

//adds a span to the div with text
return function (div_id,text){
    var div = document.getElementById(div_id);
    var span = document.createElement('span');
    span.style.cssFloat = "left";
    div.appendChild(span);
    span.textContent = text
    return span;
}(%s,%s);

//the ajax hook

return function() {
    var found_dyn = false;
    function ptq(q) {
        /* parse the query */
        var x = q.replace(/;/g, '&').split('&'), i, name, t;
        /* q changes from string version of query to object */
        for (q={}, i=0; i<x.length; i++) {
            t = x[i].split('=', 2);
            name = unescape(t[0]);
            if (!q[name])
                q[name] = [];
            if (t.length > 1) {
                q[name][q[name].length] = unescape(t[1]);
            }
        /* next two lines are nonstandard */
            else
                q[name][q[name].length] = true;
        }
        return q;
    }

    function create_div(div_id){
        var div = document.createElement('div');
        document.body.appendChild(div);
        div.setAttribute('id',div_id);
        div.style.left = '32px'; 
        div.style.top = '100px';
        div.style.position="fixed";
        div.style.color="red";
        div.style.position="fixed";
        var ul = document.createElement('ul');
        div.appendChild(ul);
        return ul;
    }

    function create_dyn_div() {
        var div = document.createElement('div');
        document.body.appendChild(div);
        div.setAttribute('id',"__dyn");
        return div;
        }

    function add_li(ul,text) {
        var li = document.createElement('li');
        ul.appendChild(li);
        li.textContent = text;
        return li;
    }
    
    console.log("create div");
    var ul = create_div("my_div");
    var dyn_div = create_dyn_div();
    console.log("add li * " + ul + " * ");
    add_li(ul,"ajax loaded");
    console.log("hook ajax");
    var origOpen = XMLHttpRequest.prototype.open;
   
    XMLHttpRequest.prototype.open = function(method,url) {
        //void open(DOMString method, DOMString url, optional boolean async, optional DOMString? user, optional DOMString? password);
        if (url.search("__dyn=")>0) {
            var q = ptq(decodeURI(url));
            if (q.__dyn) {
                dyn_div.textContent = q.__dyn;
            }}
        
        console.log('request started! ' + method + ' ' + url);        
        origOpen.apply(this, arguments);
    };
    return "loaded ajax";
}();




//hook ajax
//http://stackoverflow.com/questions/5202296/add-a-hook-to-all-ajax-requests-on-a-page
//http://ajaxref.com/ch7/xhrhijackfullprototype.html
//http://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format

//driver.execute_script("document.body.removeChild(document.getElementById('mydiv'));")

