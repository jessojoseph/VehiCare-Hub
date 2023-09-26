(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: false,
        loop: true,
        nav: true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });

    
})(jQuery);

// DOM elements
const startRecordingButton = document.getElementById('start_stop_recording');
const stopRecordingButton = document.getElementById('stop_recording');
const audioPlayer = document.getElementById('audio-player');
const recordingStatusDiv = document.getElementById('recording-status');
const convertedTextDiv = document.getElementById('converted-text');

// Audio recorder instance
let audioRecorder;

// Initialize the audio recorder
startRecordingButton.addEventListener('click', () => {
    if (!audioRecorder) {
        audioRecorder = new Recorder({
            onRecordingStart: () => {
                recordingStatusDiv.textContent = 'Recording...';
            },
            onRecordingStop: (blob) => {
                recordingStatusDiv.textContent = 'Recording stopped.';
                audioPlayer.src = URL.createObjectURL(blob);
                audioPlayer.style.display = 'block';

                // Send the audio data to the server for transcription
                sendAudioForTranscription(blob);
            }
        });

        audioRecorder.start();
        startRecordingButton.textContent = 'Stop Recording'; // Update button text
        stopRecordingButton.style.display = 'inline-block'; // Show the stop button
    } else {
        // Stop recording
        audioRecorder.stop();
        startRecordingButton.textContent = 'Start Recording'; // Update button text
        stopRecordingButton.style.display = 'none'; // Hide the stop button
    }
});

// Function to send audio data to the server for transcription
function sendAudioForTranscription(blob) {
    const formData = new FormData();
    formData.append('audio_data', blob);

    fetch('/convert-audio-to-text', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display the transcribed text
        convertedTextDiv.textContent = 'Transcribed Text: ' + data.text;
    })
    .catch(error => {
        console.error('Error transcribing audio:', error);
    });
}
