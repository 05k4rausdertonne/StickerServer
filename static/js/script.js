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
        let text = document.getElementById("ltext").value
        let bold = document.getElementById("lbold").checked
        let italic = document.getElementById("litalic").checked
        let fontSize = document.getElementById("lfontsizeoutput").value
        
        let url = new URL(window.location.href);
        url.pathname = "/label";
        url.searchParams.append("text", text);
        url.searchParams.append("bold", bold);
        url.searchParams.append("italic", italic);
        url.searchParams.append("fontsize", fontSize);

        console.log(url)
        
        fetch(url);
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