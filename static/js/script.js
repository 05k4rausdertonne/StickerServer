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
        let text = document.getElementById("ltext")
        console.log(`printing label with text "${text.value}"`)
        // do stuff
    });

    document.getElementById("ebutton").addEventListener("click", function () {
        let text = document.getElementById("etext")
        console.log(`printing label with text "${text.value}"`)
        // do stuff
    });

    document.getElementById("ibutton").addEventListener("click", function () {
        let text = document.getElementById("ifile")
        console.log(`printing label with text "${text.value}"`)
        // do stuff
    });
});