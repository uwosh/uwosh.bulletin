/*    Caret Functions     */
function getCaretEnd(obj){
    if(typeof obj.selectionEnd != "undefined"){
        return obj.selectionEnd;
    }else if(document.selection&&document.selection.createRange){
        var M=document.selection.createRange();
        var Lp=obj.createTextRange();
        Lp.setEndPoint("EndToEnd",M);
        var rb=Lp.text.length;
        if(rb>obj.value.length){
            return -1;
        }
        return rb;
    }
}
function getCaretStart(obj){
    if(typeof obj.selectionStart != "undefined"){
        return obj.selectionStart;
    }else if(document.selection&&document.selection.createRange){
        var M=document.selection.createRange();
        var Lp=obj.createTextRange();
        Lp.setEndPoint("EndToStart",M);
        var rb=Lp.text.length;
        if(rb>obj.value.length){
            return -1;
        }
        return rb;
    }
}
function setCaret(obj,l){
    obj.focus();
    if (obj.setSelectionRange){
        obj.setSelectionRange(l,l);
    }else if(obj.createTextRange){
        m = obj.createTextRange();      
        m.moveStart('character',l);
        m.collapse();
        m.select();
    }
}
/* ----------------- */

/*    Escape function ADDDDDEEEEDDD ; to end of next line   */
String.prototype.addslashes = function(){
  return this.replace((["\\\.\|\[\]\^\*\+\?\$\(\)])/g", '\\$1']));
};
String.prototype.trim = function () {
    return this.replace(/^\s*(\S*(\s+\S+)*)\s*$/, "$1");
}; 
function actb_convert_escape_chars(str) {
    // Thanks to Ak Sorpa for this function
    // When a string is assigned to innerHTML, it will be converted
    // to contain escape sequences. For example,
    // word1 & word2 is converted into word1 &amp; word2
    // The following string
    // ~!@#$%^&*()_+=-{}][:;'/><|
    // is converted into
    // ~!@#$%^&amp;*()_+=-{}][:;'/&gt;&lt;|
    // Based on this test, only conversion of & < > signs is supported
    // by this function. Improve more if necessary.

    if (!str) {
        return str;
    }

    var escape_sequences = new Object();

    escape_sequences["&lt;"] = "<";
    escape_sequences["&gt;"] = ">";
    escape_sequences["&amp;"] = "&";

    var converted = str;
    for (var esc in escape_sequences) {
        converted = converted.replace(esc, escape_sequences[esc]);
    }

    return converted;
}


function actb(obj, evt, ca, uids){
    /* ---- Variables ---- */
    var actb_timeOut = -1; // Autocomplete Timeout in ms (-1: autocomplete never time out)...changed to -1
    var actb_lim = -1;    // Number of elements autocomplete can show (-1: no limit)... changed to -1
    var actb_firstText = 0; // should the auto complete be limited to the beginning of keyword?... changed to 0
    var actb_mouse = true; // Enable Mouse Support
    var actb_delimiter = new Array(';',',');  // Delimiter for multiple autocomplete. Set it to empty array for single autocomplete
    //var actb_expand_onfocus = expand_onfocus;
    var actb_complete_on_tab = 0;//change to 0
    var actb_show_alerts = 0;//changed to 0
    /* ---- Variables ---- */

    /* --- Styles --- */
    var actb_bgColor = '#888888';
    var actb_textColor = '#FFFFFF';
    var actb_hColor = '#000000';
    var actb_fFamily = 'Verdana';
    var actb_fSize = '11px';
    var actb_hStyle = 'color:blue;text-decoration:underline;font-weight="bold"';
    /* --- Styles --- */

    /* ---- Don't touch :P---- */
    var actb_delimwords = new Array();
    var actb_cdelimword = 0;
    var actb_delimchar = new Array();
    var actb_keywords = new Array();
    var actb_uids = new Array();
    var actb_display = false;
    var actb_pos = 0;
    var actb_total = 0;
    var actb_curr = null;
    var actb_rangeu = 0;
    var actb_ranged = 0;
    var actb_bool = new Array();
    var actb_pre = 0;
    var actb_toid;
    var actb_tomake = false;
    var actb_getpre = "";
    var actb_mouse_on_list = true;
    var actb_kwcount = 0;
    var actb_caretmove = false;
    var actb_searched = new Array();

    
    /* ---- "Constants" ---- */

    
    actb_keywords = ca;
    actb_uids = uids;
    actb_curr = obj;
    
    var oldkeydownhandler = document.onkeydown;
    var oldblurhandler = obj.onblur;
    var oldkeyuphandler = obj.onkeyup;

    document.onkeydown = actb_checkkey;
    obj.onblur = actb_clear;
    obj.onkeyup = actb_keypress;

    setTimeout(function(){actb_tocomplete(188)},150);

        function actb_clear(evt){
        var found = false;
        if (actb_show_alerts) {
                var value = actb_curr.value;
                if (value == '') {
                    found = true;
                } else {
                        for (var i=0; i<actb_keywords.length; i++) {
                            if (value == actb_keywords[i]) {
                                found = true;
                                break;
                            }
                        }
                }
        }

        if (!evt) evt = event;
        document.onkeydown = oldkeydownhandler;
        actb_curr.onblur = oldblurhandler;
        actb_curr.onkeyup = oldkeyuphandler;
        actb_removedisp();
    }

    function actb_removedisp(){
        if (!actb_mouse_on_list){
            actb_display = false;
            if (actb_toid) clearTimeout(actb_toid);
        }
    }


    function actb_parse(n){
        if (actb_delimiter.length > 0){
            var t = actb_delimwords[actb_cdelimword].trim().addslashes();
            var plen = actb_delimwords[actb_cdelimword].trim().length;
        }else{
            var t = actb_curr.value.addslashes();
            var plen = actb_curr.value.length;
        }
        var tobuild = '';
        var i;

        if (actb_firstText){
            var re = new RegExp("^" + t, "i");
        }else{
            var re = new RegExp(t, "i");
        }
        var p = n.search(re);
        
	if (p != -1)
	  {
        for (i=0;i<p;i++){
            tobuild += n.substr(i,1);
        }
        for (i=p;i<n.length;i++){
            tobuild += n.substr(i,1);
        }
	  }
        return tobuild;
    }
    function curTop(){
        actb_toreturn = 0;
        obj = actb_curr;
        while(obj){
            actb_toreturn += obj.offsetTop;
            obj = obj.offsetParent;
        }
        return actb_toreturn;
    }
    function curLeft(){
        actb_toreturn = 0;
        obj = actb_curr;
        while(obj){
            actb_toreturn += obj.offsetLeft;
            obj = obj.offsetParent;
        }
        return actb_toreturn;
    }
    
    function determineWidth(){
       var max=0;
       for (i=0;i<actb_keywords.length;i++){
          lenkw=actb_keywords[i].length;
          if (lenkw>max)
          { max = lenkw }
       }
       max++;
       return max.toString()+'em';
    }

//     function actb_hideWords() {
//       var matches = new Array();//get matches... with each option iterate over matches... if in matches then display block
//       var optLength = document.getElementById('assocFaculty_options').length;
      
//       for (i=0;i<actb_keywords.length;i++)
//       	{
//       	matches[i] = actb_parse(actb_keywords[i]);
// 	}
//       for (var j = 0; j < optLength; j++)
// 	  {
// 	    option = document.getElementById('assocFaculty_options').options[j].text;
// 	    if (actb_searched[j] === false)
// 	      {
// 	    for (var k = 0; k < matches.length; k++)
// 	      {
// 		if (matches[k] == ''){continue;}
// 		if (option == matches[k])
// 		  {
// 		    document.getElementById('assocFaculty_options').options[j].style.display = "block";//set an attribute
// 		    actb_searched[j] = true;
// 		    continue;
// 		  }
// 		if (option != matches[k] && actb_searched[j] === true)
// 		  {
// 		    continue;
// 		  }
		
// 		if (option != matches[k])
// 		  {
// 		    document.getElementById('assocFaculty_options').options[j].style.display = "none";
// 		  }
// 	      }
// 	    if (actb_searched[j] === true)
// 	      {
// 		continue;
// 	      }
// 	      }
// 	  }

//         }

    function get_matches() {
      var matches = new Array();
      for (i=0;i<actb_keywords.length;i++)
       	{
	  matches[i] = actb_parse(actb_keywords[i]);//lookup uid in actb_parse when found
 	}///add some efficiency logic once this works
      return matches;
    }

    function get_match_uid(match)
    {
      match_index = actb_keywords.indexOf(match);
      return actb_uids[match_index];
    }

    function clear_options(widget_id)
    {
      //remove all options...after done refactor this
      list=document.getElementById(widget_id + "_options");
      //for (var x=list.length-1; x >= 0; x--) { //this works as well//if uid not in list remove it
      //list.remove(x);}
      list.options.length=0;
    }

    function rebuild_options(widget_id, uid, label)
    {
      var inList = false;
      // check if the item isn't already in the list <--- NEED TO DO THIS TO AVOID DUPLICATION... get all values currently in select
      var current_values = cssQuery('.' + widget_id + "_option");//test
      for (var i=0; i < current_values.length; i++) {
	if (current_values[i].value == uid) {
	  inList = true;//need to iterate over all values
	}
      }
      
      if (inList == false)
	{	  
	  options = document.getElementById(widget_id + "_options");
	  option = document.createElement('option');
	  option.value = uid;
	  option.text = label;
	  option.className = widget_id + "_option";
	  options.appendChild(option);
	}
	  
      }         


  
    

    function refresh_options() {
      matches = get_matches();
      var cm = 0;
      list=document.getElementById("assocFaculty_options");
      for (x=0;x<matches.length;x++)
	{
	  if (matches[x] != '')
	    {
	      cm++;
	    }
	}
      if (cm != list.length)
	{//better yet check if matches are different than options
      clear_options('assocFaculty');
      //make sure it is not selected
      for (x=0;x<matches.length;x++)
	{
	  if (matches[x] != '')
	    {
	      match_uid = get_match_uid(matches[x]);
	      //alert("Match:" + matches[x] + "MatchUID" + match_uid);
	      rebuild_options('assocFaculty', match_uid, matches[x], 1);
	    }
	}
	}
    }
    
    function actb_keypress(){
        return !actb_caretmove;
    }

    function actb_checkkey(evt){
        if (!evt) evt = event;
        a = evt.keyCode;
        caret_pos_start = getCaretStart(actb_curr);
        actb_caretmove = 0;
        switch (a){
            case 27:  // esc to show the menu
                setTimeout(function(){actb_tocomplete(a)},50);
                break
	case 13://enter key pressed
                //actb_caretmove = 1;
                return false;
                break;
	case 9://tab
                if (actb_complete_on_tab && actb_display) {
		  //actb_penter();
		  //actb_caretmove = 1;
                    return false;
                    break;
                } else {
                  break
                }
            default:
                setTimeout(function(){actb_tocomplete(a)},50);
                break;
        }
    }

    function actb_tocomplete(kc){
        if (kc == 38 || kc == 40 || kc == 13) return;
        var i;
        if (actb_display){ 
            var word = 0;
            var c = 0;
            for (var i=0;i<=actb_keywords.length;i++){
                if (actb_bool[i]) c++;
                if (c == actb_pos){
                    word = i;
                    break;
                }
            }
            actb_pre = word;
        }else{ actb_pre = -1};
        
        actb_mouse_on_list = 0;
        //if (actb_curr.value == ''){
            //actb_mouse_on_list = 0;
            //return;
        //}
        if (actb_delimiter.length > 0){
            caret_pos_start = getCaretStart(actb_curr);
            caret_pos_end = getCaretEnd(actb_curr);
            
            delim_split = '';
            for (i=0;i<actb_delimiter.length;i++){
                delim_split += actb_delimiter[i];
            }
            delim_split = delim_split.addslashes();
            delim_split_rx = new RegExp("(["+delim_split+"])");
            c = 0;
            actb_delimwords = new Array();
            actb_delimwords[0] = '';
            for (i=0,j=actb_curr.value.length;i<actb_curr.value.length;i++,j--){
                if (actb_curr.value.substr(i,j).search(delim_split_rx) == 0){
                    ma = actb_curr.value.substr(i,j).match(delim_split_rx);
                    actb_delimchar[c] = ma[1];
                    c++;
                    actb_delimwords[c] = '';
                }else{
                    actb_delimwords[c] += actb_curr.value.charAt(i);
                }
            }

            var l = 0;
            actb_cdelimword = -1;
            for (i=0;i<actb_delimwords.length;i++){
                if (caret_pos_end >= l && caret_pos_end <= l + actb_delimwords[i].length){
                    actb_cdelimword = i;
                }
                l+=actb_delimwords[i].length + 1;
            }
            var t = actb_delimwords[actb_cdelimword].addslashes().trim();
        }else{
            var t = actb_curr.value.addslashes();
        }
        if (actb_firstText){
            var re = new RegExp("^" + t, "i");
        }else{
            var re = new RegExp(t, "i");
        }
        
        actb_total = 0;
        actb_tomake = false;
        actb_kwcount = 0;
        for (i=0;i<actb_keywords.length;i++){
            actb_bool[i] = false;
            if (re.test(actb_keywords[i])){
                actb_total++;
                actb_bool[i] = true;
                actb_kwcount++;
                if (actb_pre == i) actb_tomake = true;
            }
        }
        if (actb_toid) clearTimeout(actb_toid);
        if (actb_timeOut > 0) actb_toid = setTimeout(function(){actb_mouse_on_list = 0;},actb_timeOut);
	for (i=0;i<actb_keywords.length;i++) 
	  {
	    actb_searched[i] = false;
	  }
        refresh_options();//going to have to pass uid as well as the text of the field so i can add and remove references

    }
}

/*    InAndOut Widget JS     */

function inout_selectAllWords(theList) {
  myList = document.getElementById(theList);
  for (var x=0; x < myList.length; x++) {
    myList[x].selected="selected";
  }
}

function inout_addNewKeyword(toList, newText, newValue) {
  theToList=document.getElementById(toList);
  for (var x=0; x < theToList.length; x++) {
    if (theToList[x].text == newText) {
      return false;
    }
  }
  theLength = theToList.length;
  theToList[theLength] = new Option(newText);
  theToList[theLength].value = newValue;
  theToList[theLength].className = "assocFaculty_option";
}

function inout_moveKeywords(fromList,toList,selectThese) {
  theFromList=document.getElementById(fromList);
  for (var x=0; x < theFromList.length; x++) {
    if (theFromList[x].selected) {
      inout_addNewKeyword(toList, theFromList[x].text, theFromList[x].value);
    }
  }
  theToList=document.getElementById(fromList);
  for (var x=theToList.length-1; x >= 0 ; x--) {
    if (theToList[x].selected) {
      theToList[x] = null;
    }
  }
  inout_selectAllWords(selectThese);
}

//add and remove references javascript//
//
//


// function to clear the reference field or remove items
// from the multivalued reference list.
// function referencebrowser_removeReference(widget_id, multi)
// {
//     if (multi) {
//         list=document.getElementById(widget_id)
//         for (var x=list.length-1; x >= 0; x--) {
//           if (list[x].selected) {
//             list[x]=null;
//           }
//         }
//         for (var x=0; x < list.length; x++) {
//             list[x].selected='selected';
//           }        
//     } else {
//         element=document.getElementById(widget_id);
//         label_element=document.getElementById(widget_id + '_label');
//         label_element.value = "";
//         element.value="";
//     }
// }


