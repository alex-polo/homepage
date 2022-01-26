
function main(){
    hideSpinner()
}

if (window.addEventListener) // W3C standard
    window.addEventListener('load', main, false)
else if (window.attachEvent) // Microsoft
    window.attachEvent('onload', main)