window.onload = function(){
    var lisF = document.getElementById("navs");
    var lis = lisF.getElementsByTagName("li");
    var tabsF = document.getElementById("tabs");
    var tabs = tabsF.children;
    for(var i=0;i<lis.length;i++){
        lis[i].index = i;
        lis[i].onmouseover = function(){
            show(this.index);
        }
    }
    function show(a){
        for(var j=0;j<lis.length;j++){
            lis[j].classList.remove("active");
            tabs[j].classList.remove("in");
            tabs[j].classList.remove("active");
        }
        lis[a].classList.add("active");
        tabs[a].classList.add("in");
        tabs[a].classList.add("active");
    }
}
$('.alert').fadeOut(2000);