$(".sectionsort .dropdown-menu li a").click(function(){
    $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
    $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
});

//make sure height of left and right panel is equal
window.onload = function(){
    var leftheight = document.getElementById('panel-left').offsetHeight;
    var rightheight = document.getElementById('panel-right').offsetHeight;
    if (rightheight - leftheight > 0) {
        document.getElementById('panel-left').style.height = rightheight + 'px';
    }
}

$(function(){
  $(window).scroll(function(){
    var curpos = $(this).scrollTop()
    var maxTop = 110;
    if (curpos > maxTop) {
        $("#sidebar").addClass('sticky');
    }
    else {
        $("#sidebar").removeClass('sticky');
    }
  });
});