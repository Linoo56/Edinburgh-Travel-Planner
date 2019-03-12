'use strict';

$(function() {
    
    //Config
    var width = 400;
    var animationSpeed = 1400;
    var pause = 4000;
    var currentSlide = 1;
    
    var $slider = $('#slider');
    var $slideContainer = $slider.find('.slides');
    var $slides = $slideContainer.find('.slide');
    
    setInterval(function() {
        $slideContainer.animate({'margin-left': '-='+width}, animationSpeed, function() {
            currentSlide++;
            if (currentSlide === $slides.length) {
                currentSlide = 1;
                $slideContainer.css('margin-left', 0);
            }
        });
    }, pause);
    
    
    //setInterval
    //Animage margin left
    //If last slide go to position 1
    //listen for mouseenter and pause
})