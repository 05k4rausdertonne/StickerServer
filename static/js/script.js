// static/js/script.js
function removeFE0F(str) {
    return str.replace(/\uFE0F/g, '');
}

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
            
        if (text != '') {
            let url = new URL(window.location.href);
            url.pathname = "/label";
            url.searchParams.append("text", text);
            url.searchParams.append("bold", bold);
            url.searchParams.append("italic", italic);
            url.searchParams.append("fontsize", fontSize);

            console.log(url)
            
            fetch(url.href);
        }
    });

    document.getElementById("ebutton").addEventListener("click", function () {
        let text = removeFE0F(document.getElementById("etext").value)
            
        if (text != '') {
            let url = new URL(window.location.href);
            url.pathname = "/label";
            url.searchParams.append("text", text);
            url.searchParams.append("emoji", true);

            console.log(url)
            
            fetch(url.href);
        }
    });

    document.getElementById("ibutton").addEventListener("click", function () {
        let text = document.getElementById("ifile")
        // TODO: do stuff
    });
});