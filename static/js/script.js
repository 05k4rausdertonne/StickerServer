// static/js/script.js
function removeFE0F(str) {
    return str.replace(/\uFE0F/g, '');
}

document.addEventListener('DOMContentLoaded', function() {
    // Access the root element where the variables are defined
    const root = document.querySelector(':root');
    const rootStyles = getComputedStyle(root);
    const color1 = rootStyles.getPropertyValue('--color-1').trim();
    const color2 = rootStyles.getPropertyValue('--color-2').trim();
    const color3 = rootStyles.getPropertyValue('--color-3').trim();
    const color4 = rootStyles.getPropertyValue('--color-4').trim();
    const color5 = rootStyles.getPropertyValue('--color-5').trim();

    // Tab switching logic
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetContent = document.getElementById(targetId);

            if (!targetContent) return;

            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and target content
            this.classList.add('active');
            targetContent.classList.add('active');
        });
    });

    let sliders = document.getElementsByClassName('rangeslider');
    for (let slider of sliders)  {
        let output = document.getElementById(`${slider.id}output`)
        slider.addEventListener('input', function  () {
            output.value = slider.value;
        });
    }

    document.getElementById('lbutton').addEventListener('click', async function () {
        let text = document.getElementById('ltext').value
        let bold = document.getElementById('lbold').checked
        let italic = document.getElementById('litalic').checked
        let fontSize = document.getElementById('lfontsizeoutput').value
            
        if (text != '') {
            let url = new URL(window.location.href);
            url.pathname = '/label';
            url.searchParams.append('text', text);
            url.searchParams.append('bold', bold);
            url.searchParams.append('italic', italic);
            url.searchParams.append('fontsize', fontSize);
            
            console.log(url)
            
            fetch(url.href).then(response => {
                if (response.ok) {
                    return response.statusText;
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });
        }
        else {
            alert('Please enter text before submitting.');
        }
    });

    document.getElementById('ebutton').addEventListener('click', async function () {
        let text = removeFE0F(document.getElementById('etext').value)
            
        if (text != '') {
            let url = new URL(window.location.href);
            url.pathname = '/label';
            url.searchParams.append('text', text);
            url.searchParams.append('emoji', true);
            
            console.log(url)
            
            fetch(url.href).then(response => {
                if (response.ok) {
                    return response.statusText;
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });
        }
        else {
            alert('Please enter emoji(s) before submitting.');
        }
    });

    document.getElementById('iform').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission
        const fileInput = document.getElementById('ifile');
        let autoRotate = document.getElementById('iautorotate').checked
        let edgeEnhance = document.getElementById('iedgeenhance').checked
    
        const file = fileInput.files[0];
    
        if (!file) {
            alert('Please select a file before submitting.');
            return;
        }
    
        const formData = new FormData();
        formData.append('file', file);
        let url = new URL(window.location.href);
        url.pathname = '/image';
        url.searchParams.append('autorotate', autoRotate);
        url.searchParams.append('edgeenhance', edgeEnhance);
    
        console.log(url);
    
        try {
            fetch(url.href, {
                method: 'POST',
                body: formData,
                
            }).then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    });

    document.getElementById('qrtext').value = "";
    var qrcode = new QRCode('qrdiv', {
        text: "http://makestickers.local/",
        colorDark : color1,
        colorLight : color5
    });
    var qrcodeinvisible = new QRCode('qrinvisible', {
        text: "http://makestickers.local/",
        width: 384,
        height: 384,
        colorDark : "#000000",
        colorLight : "#ffffff"
    });

    document.getElementById('qrtext').addEventListener('input', async function () {
        qrcode.clear(); 
        qrcodeinvisible.clear();
        let text = document.getElementById('qrtext').value;
        
        if (text == '') {
            qrcode.makeCode('http://makestickers.local/');
            qrcodeinvisible.makeCode('http://makestickers.local/');
        }
        else {
            qrcode.makeCode(text);
            qrcodeinvisible.makeCode(text);
        }
    });

    document.getElementById('qrbutton').addEventListener('click', async function () {
        let canvas = document.getElementById('qrinvisible').getElementsByTagName('canvas')[0];
        let url = new URL(window.location.href);
        url.pathname = '/image';
        canvas.toBlob(function(blob) {
            const formData = new FormData();
            formData.append('file', blob, 'image.png');
            fetch(url.href, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });
        }, 'image/png'); 
    });

    document.getElementById('spiceform').addEventListener('submit', async function(event) {
        event.preventDefault();
        const text = document.getElementById('spicetext').value;
        const file = document.getElementById('spicefile').files[0];
        const bold = document.getElementById('spicibold').checked;
        const italic = document.getElementById('spicitalic').checked;
        const fontSize = document.getElementById('spicesize').value;
        const autoRotate = document.getElementById('spiceautorotate').checked;
        const edgeEnhance = document.getElementById('spiceedgeenhance').checked;

        const formData = new FormData();
        formData.append('text', text);
        if (file) {
            formData.append('file', file);
        }
        formData.append('bold', bold);
        formData.append('italic', italic);
        formData.append('fontsize', fontSize);
        formData.append('autorotate', autoRotate);
        formData.append('edgeenhance', edgeEnhance);

        try {
            const response = await fetch('/spice-jar', {
                method: 'POST',
                body: formData,
            });
            if (response.ok) {
                const data = await response.json();
                console.log('Spice Jar Success:', data);
            } else {
                throw new Error('Network response was not ok.');
            }
        } catch (error) {
            console.error('Error submitting spice jar:', error);
        }
    });

});