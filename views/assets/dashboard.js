function expand(app) {
    const info = document.getElementById(app + '-info');
    if (info.style.display === 'none') {
        info.style.display = 'flex';
    }
    else {
        info.style.display = 'none'
    }
}

function copy(id) {
    const text = document.getElementById(id + '-token').innerText;
    const el = document.createElement('textarea');
    el.value = text;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}