// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {

    let sliders = document.getElementsByClassName("rangeslider");

    sliders.forEach(slider=> {
        let output = document.getElementsById(`${slider.id}output`)
        slider.addEventListener("input", function  () {
            output.value = slider.value;
        });
    });

    document.getElementsById("lbutton").addEventListener("click", function () {
        
        console.log(`printing label with text "${form.elements.ltext.value}"`)
        // do stuff
    });

});