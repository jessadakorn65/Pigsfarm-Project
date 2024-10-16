$(document).ready(function () {
    // Toggle sidebar
    $(".fa-bars").click(function () {
        $(".nav-screen").animate({ right: "0px" }, 200);
        $("body").animate({ right: "285px" }, 200);
    });
    $(".fa-times").click(function () {
        $(".nav-screen").animate({ right: "-285px" }, 200);
        $("body").animate({ right: "0px" }, 200);
    });

    // Smooth scrolling
    $('a[href^="#"]').on('click', function(event) {
        event.preventDefault();
        const target = this.hash;
        $('html, body').animate({
            scrollTop: $(target).offset().top
        }, 800);
    });

    // Initialize fullPage.js
    new fullpage('#fullpage', {
        navigation: true,
        scrollBar: true,
        afterLoad: function (origin, destination, direction) {
            if (destination.index === 1) {
                // Additional functionality for second section
                console.log("Section 2 loaded");
            }
        }
    });
});
