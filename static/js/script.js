// static/js/script.js
function removeFE0F(str) {
    return str.replace(/\uFE0F/g, '');
}

document.addEventListener('DOMContentLoaded', function() {

    // Access the root element where the variables are defined
    const root = document.querySelector(':root');

    // Get the computed style of the root element
    const rootStyles = getComputedStyle(root);

    // Access the variables using their names
    const color1 = rootStyles.getPropertyValue('--color-1').trim();
    const color2 = rootStyles.getPropertyValue('--color-2').trim();
    const color3 = rootStyles.getPropertyValue('--color-3').trim();
    const color4 = rootStyles.getPropertyValue('--color-4').trim();
    const color5 = rootStyles.getPropertyValue('--color-5').trim();

    document.getElementById('qrdiv').getElementsByTagName('img')[0].class='qrimage';

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
            
            const response = await fetch(url.href);

            // Check if the request was successful
            if (response.ok) {
                console.log('Server response:', response.statusText);
            } else {
                console.log('Server error:', response.statusText);
                alert('Server error:', response.statusText);
            }
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
            
            const response = await fetch(url.href);

            // Check if the request was successful
            if (response.ok) {
                console.log('Server response:', response.statusText);
            } else {
                console.log('Server error:', response.statusText);
                alert('Server error:', response.statusText);
            }
        }
        else {
            alert('Please enter emoji(s) before submitting.');
        }

    });


    document.getElementById('iform').addEventListener('submit', async function(event) {
        event.preventDefault();  // Prevent the default form submission
    
        // Get the file input element
        const fileInput = document.getElementById('ifile');

        let autoRotate = document.getElementById('iautorotate').checked
        let edgeEnhance = document.getElementById('iedgeenhance').checked
    
        // Get the selected file from the input element
        const file = fileInput.files[0];
    
        if (!file) {
            alert('Please select a file before submitting.');
            return;
        }
    
        // Create a FormData object to hold the file
        const formData = new FormData();
        formData.append('file', file);

        let url = new URL(window.location.href);
        url.pathname = '/image';
        url.searchParams.append('autorotate', autoRotate);
        url.searchParams.append('edgeenhance', edgeEnhance);

        console.log(url);
    
        try {
            // Send the file using fetch with a POST request
            const response = await fetch(url.href, {
                method: 'POST',
                body: formData,
                
            });
    
            // Check if the request was successful
            if (response.ok) {
                const result = await response.json();
                console.log('Server response:', result);
            } else {
                console.log('Server error:', response.statusText);
            }
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

    

    document.getElementById('qrtext').addEventListener('input', async function () {
        qrcode.clear(); // clear the code.
        let text = document.getElementById('qrtext').value;

        // console.log(`qr text: ${text}`);
        
        if (text == '') {
            qrcode.makeCode('http://makestickers.local/');
        }
        else {
            qrcode.makeCode(text);
        }
    });

    document.getElementById('qrbutton').addEventListener('click', async function () {
        
        console.log(document.getElementById('qrdiv').getElementsByTagName('img')[0]);
        
    });
});