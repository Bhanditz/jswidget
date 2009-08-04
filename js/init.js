var stylesheetURL = 'base-widget-style.css?bsvar=7'

//thanks, http://www.ibm.com/developerworks/xml/library/x-matters41.html
function prependChild(parent, node) {
    parent.insertBefore(node, parent.firstChild);
}

//insert a stylesheet before all other stylesheets
//more precisely, it inserts the stylesheet at the beginning of head
//this way, it is overriden by other stylesheets
function cc_js_insert_stylesheet_first(stylesheetURL){

    //build our stylesheet link node
    var cssNode = document.createElement('link');
    cssNode.type = 'text/css';
    cssNode.rel = 'stylesheet';
    cssNode.href = stylesheetURL;
    cssNode.media = 'screen';
    cssNode.title = 'dynamicLoadedSheet';
    
    //shove it in there!
    prependChild(document.getElementsByTagName("head")[0], cssNode);
}

function cc_js_pageInit() {
   //no peeking! (the widget is hidden by default)

    cc_js_init_tip();

    //shove our stylesheet in before all the others
    cc_js_insert_stylesheet_first(stylesheetURL);

    cc_js_apply_extras();

   //ok, you can look now
   cc_js_$('generated_box').style.display = '';
}

if (window.onload) {
    old_onload = window.onload;
    window.onload = function () {
	old_onload();
	cc_js_pageInit();
    }
}
else {
    window.onload = cc_js_pageInit;
}

