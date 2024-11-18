   

    $(".FileInput").on('change',function (e) {
        var labelVal = $(".title").text();
        var oldfileName = $(this).val();
            fileName = e.target.value.split( '\\' ).pop();

            if (oldfileName == fileName) {return false;}
            var extension = fileName.split('.').pop();

        if ($.inArray(extension,['jpg','jpeg','png']) >= 0) {
            $(".filelabel i").removeClass().addClass('fa fa-file-image-o');
            $(".filelabel i, .filelabel .title").css({'color':'#208440'});
        }
        else if(extension == 'pdf'){
            $(".filelabel i").removeClass().addClass('fa fa-file-pdf-o');
            $(".filelabel i, .filelabel .title").css({'color':'red'});

        }
else if(extension == 'doc' || extension == 'docx'){
        $(".filelabel i").removeClass().addClass('fa fa-file-word-o');
        $(".filelabel i, .filelabel .title").css({'color':'#2388df'});
    }
        else{
            $(".filelabel i").removeClass().addClass('fa fa-file-o');
            $(".filelabel i, .filelabel .title").css({'color':'black'});
        }

        if(fileName ){
            if (fileName.length > 10){
                $(".filelabel .title").text(fileName.slice(0,4)+'...'+extension);
            }
            else{
                $(".filelabel .title").text(fileName);
            }
        }
        else{
            $(".filelabel .title").text(labelVal);
        }
    });
$(document).ready(function () {

    function equalcard(s) {
        var h = 0;
            var line_height = 0;
            $(s).css("display", "block").css("height", "auto");
            $(s).each(function () {
                  var height = $(this).outerHeight(true);
              if (height > h) {
                    h = height;
               }
        });
        $(s).height(h);
      }
    //   equalcard("#testimonial section.wrapper ul li div.bottom");
      equalcard("#team section.wrapper ul li div.team-content p");
      equalcard("#team section.wrapper ul li div.team-content div.social-icons");
      equalcard("#career section.wrapper div.career-bottom ul li h3");
      

    // $(".main-slider").slick({
    //     infinite: true,
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     autoplay: false,
    //     autoplaySpeed: 4000,
    // }); 

    
    function MySlickA() {
        let len = $("#facilities .wrapper .facility-slider-box li").length;
        let direction = $(".facility-slider-box").attr("data-rtl");
        if (len > 3) {
            $(".facility-slider-box").slick({
                autoplay: true,
                infinite: true,
                slidesToShow: 3,
                slidesToScroll: 1,
                arrows: true,
                dots: false,
                responsive: [
                    {
                        breakpoint: 981,
                        settings: {
                            slidesToShow: 2,
                            infinite: true,
                            dots: true,
                        },
                    },
                    {
                        breakpoint: 641,
                        settings: {
                            slidesToShow: 1,
                            infinite: true,
                            dots: true,
                        },
                    },
                ],
            });
        }
    }
    MySlickA();
    // testmonial-slider

    function MySlick() {
        let len = $("#testimonial section.wrapper ul li").length;
        let direction = $(".testimonial-slider-box").attr("data-rtl");
        console.log("testimoial slider");
        if (len > 4) {
            $(".testimonial-slider-box").slick({
                infinite: true,
                slidesToShow: 4,
                slidesToScroll: 2,
                arrows: true,
                autoplay: true,
                dots: true,
                responsive: [
                    {
                        breakpoint: 1181,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 2,
                            infinite: true,
                            dots: true,
                        },
                    },
                    {
                        breakpoint: 981,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 2,
                            infinite: true,
                            dots: true,
                        },
                    },
                    {
                        breakpoint: 641,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1,
                            infinite: true,
                            dots: true,
                        },
                    },
                    {
                        breakpoint: 481,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            infinite: true,
                            dots: true,
                        },
                    },
                ],
            });
        }
    }
    MySlick();

    function MySlick2() {
        let len = $("#department section.wrapper div.department-card ul li.card").length;
        let direction = $(".department-slider-box").attr("data-rtl");
        if (len > 2) {

            $(".department-slider-box").slick({
                infinite: true,
                slidesToShow: 2,
                slidesToScroll: 1,
                autoplay: true,
                arrows: true,
                dots: true,
                responsive: [
                    {
                        breakpoint: 981,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            infinite: true,
                            dots: true,
                        },
                    },
                ],
            });
        }
    }
    MySlick2();


    function MySlick3() {
        let len = $(".activity-slider li").length;
        let direction = $(".activity-slider").attr("data-rtl");
        if (len > 3) {
            $(".activity-slider").slick({
                infinite: true,
                slidesToShow: 3,
                slidesToScroll: 3,
                arrows: true,
                dots: true,
                responsive: [
                    {
                        breakpoint: 981,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1,
                            infinite: true,
                            dots: true,
                        },
                    },
                    {
                        breakpoint: 641,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            infinite: true,
                            dots: true,
                        },
                    },
                ],
            });
        }
    }
    MySlick3();
});

// header scroll fixed
$(window).scroll(function () {
    var scroll_pos = 0;

    scroll_pos = $(this).scrollTop();

    if (scroll_pos > 0) {
        $("header").css("background-color", "#5BBA64");
        $("header").css("box-shadow", "rgb(68 68 68 / 5%) 2px 3px 3px");
    } else if (scroll_pos == 0) {
        $("header").removeAttr("style");
    }
});
function showGallery(evt, imagename) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("year");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    (document.getElementById(imagename).style.display = "flex"),
        (evt.currentTarget.className += " active");
}
let menu_icon = document.querySelector("#menu-icon");
let menu_container = document.querySelector("#mobile-menu");
let overlay_container = document.querySelector("#overlay");
menu_icon.addEventListener("click", () => {
    menu_container.classList.toggle("active");
});
menu_icon.addEventListener("click", () => {
    overlay_container.classList.toggle("active");
});

function closeIcon() {
    document.getElementById("overlay").classList.remove("active");
    document.getElementById("mobile-menu").classList.remove("active");
}

// function closeOverlay() {
//     document.getElementById("overlay").classList.remove("active");
// }

function showItems(evt, imagename) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("image-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("items");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    (document.getElementById(imagename).style.display = "flex"),
        (evt.currentTarget.className += " active");
}
