console.log('connected')

stripUSD = function (num) {
    if (typeof (num) == 'string') {
        num = num.replace('$', '').replaceAll(',', '');
        return parseInt(num);
    }
}

let total = document.getElementById('total');
let values = document.querySelectorAll('#value');
let calculateTotal = 0;

values.forEach(value => {
    num = stripUSD(value.innerHTML);
    calculateTotal += num;
})

total.innerHTML = '$' + calculateTotal.toLocaleString('en-US');

