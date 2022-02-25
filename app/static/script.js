/* window.onload = function(){
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
} */
$('.alert').fadeOut(2000);
window.onload = function(){
	var lis = document.getElementsByClassName("page");
	for(var i=0;i<lis.length;i++){
		lis[i].index = i;
        lis[i].onclick = function(){
            change(this.index);
		}
	}
	function change(a){
		for(var i=0;i<lis.length;i++){
            lis[i].classList.remove("active");
		}
		lis[a].classList.add("active");
	}
	/* 上一页和下一页的切换 */
	/* 下一页 */
	var btn1 = document.getElementsByClassName("next")[0];
	var next = btn1.firstChild;
	var active_li = document.getElementById('target');
	var next_href = active_li.nextElementSibling.firstElementChild.href;
	/* 最后一页*/
	if(active_li.nextElementSibling.className == 'next'){
		btn1.classList.remove("next");
		btn1.classList.add("disabled")
		}
	else{next.href = next_href;}
	/* 上一页 */
	var btn2 = document.getElementsByClassName("previous")[0];
	var previous = btn2.firstChild;
	var previous_href = active_li.previousElementSibling.firstElementChild.href;
	/* 第一页 */
	if(active_li.previousElementSibling.className == 'previous'){
		btn2.classList.remove("previous");
		btn2.classList.add("disabled")
		}
	else{previous.href = previous_href;}	
}