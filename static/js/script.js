// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {

    let sliders = document.getElementsByClassName("rangeslider");

    for (let slider of sliders)  {
        let output = document.getElementById(`${slider.id}output`)
        slider.addEventListener("input", function  () {
            output.value = slider.value;
        });
    }

    document.getElementById("lbutton").addEventListener("click", function () {
        
        console.log(`printing label with text "${form.elements.ltext.value}"`)
        // do stuff
    });

});