for (let i = 0; i < 32; i++) {
    for (let j = 0; j < 32; j++) {
        document.querySelector('.main__grid').insertAdjacentHTML('beforeend', `<div class="main__cell" id="cell-${i * 32 + j}"></div>`);
    }
}

document.querySelector('.main__right--input').addEventListener('change', () => {
    document.querySelector('.main__right--label').style.backgroundColor = 'bisque';
    document.querySelector('.main__right--label').style.color = 'black';
    document.querySelector('.main__right--label').innerHTML = '&checkmark; Selected';
})

const runNetwork = async pixels => {
    const fetched = await fetch('http://127.0.0.1:5000/api/ml', {
        method: 'POST',
        body: JSON.stringify({data: pixels}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const response = await fetched.json();

    return response;
}

const classes = ['flowers', 'food containers', 'fruits', 'electronics', 'furniture', 'people', 'trees', 'vehicles'];

document.querySelector('.main__right--form').addEventListener('submit', e => {
    e.preventDefault();
    document.querySelector('.main__right--label').style.backgroundColor = '#555';
    document.querySelector('.main__right--label').style.color = 'white';
    document.querySelector('.main__right--label').innerHTML = 'Select your image';
    if (document.querySelector('.main__right--input').files.length == 0) {
        alert('No image selected.');
        return;
    }
    const reader = new FileReader();
    reader.readAsDataURL(document.querySelector('.main__right--input').files[0]);
    reader.addEventListener('load', () => {
        const canvas = document.querySelector('.main__canvas');
        const context = canvas.getContext('2d');
        const img = new Image();
        img.addEventListener('load', async () => {
            context.drawImage(img, 0, 0);
            const data = [...context.getImageData(0, 0, 32, 32).data];
            let pixels = [];
            let index = 0;
            let cellindex = 0;
            for (let i = 0; i < 32; i++) {
                let cur = [];
                for (let j = 0; j < 32; j++) {
                    let innercur = [];
                    for (let k = 0; k < 3; k++) {
                        innercur.push(data[index++]);
                        if (index % 4 == 3) index++;
                    }
                    cur.push(innercur);
                    document.getElementById(`cell-${cellindex}`).style.backgroundColor = `rgb(${innercur[0]}, ${innercur[1]}, ${innercur[2]})`;
                    cellindex++;
                }
                pixels.push(cur);
            }
            const pred = await runNetwork(pixels);

            const results = pred.result.map(parseFloat);

            const byClass = results.map((el, ind) => [el, ind]);
            byClass.sort((a, b) => b[0] - a[0]);
            while (document.querySelector('.main__right--heading')) document.querySelector('.main__right--heading').remove();
            while (document.querySelector('.main__right--desc')) document.querySelector('.main__right--desc').remove();
            while (document.querySelector('.main__right--others')) document.querySelector('.main__right--others').remove();
            document.querySelector('.main__right--form').insertAdjacentHTML('beforebegin', `<h2 class="main__right--heading">Results</h2>
            <p class="main__right--desc">The model thinks your image is of <strong>${classes[byClass[0][1]]}</strong>.</p>
            <p class="main__right--desc">Wrong? Here's how it considers the other possibilities:</p>
            <ul class="main__right--others">
                ${byClass.map(el => `<li class="main__right--other">${classes[el[1]]} (${((el[0]*100/0.1)|0)/10}%)</li>`).join('')}
            </ul>`);
            document.querySelector('.main__right--other').className += ' main__right--pred';
        })
        img.src = reader.result;
    })
})