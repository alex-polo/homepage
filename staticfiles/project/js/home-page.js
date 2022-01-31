// const endpointTimeUrl = currentLocation.href + '/home/time'
const endpointTimeUrl = window.location + '/home/time'


function isInternetExplorer() {
    return window.navigator.userAgent.indexOf('MSIE ') > -1 || window.navigator.userAgent.indexOf('Trident/') > -1;
}


// // Update time
// function updateHtmlTimeContainer(serverResponse) {
//     document.getElementById('time_container').textContent = serverResponse.time
// }

// async function synceTime() {
//     synceWithServer(endpointTimeUrl, updateHtmlTimeContainer)
// }


// --------------------------------------------------------
// Spinner show, hide functions
function hideSpinner() {
    let spinner = document.getElementById('spinner')
    if (spinner != null) {
        spinner.style.visibility = 'hidden'
    }
}

function showSpinner() {
    let spinner = document.getElementById('spinner')
    spinner.style.visibility = 'visible';
}

// --------------------------------------------------------


function main() {
    if (isInternetExplorer()) {
        window.MSInputMethodContext && document.documentMode && document.write(
            '<link rel="stylesheet" href="static/bootstrap-ie11/css/bootstrap-ie11.min.css">' +
            '<script type="text/javascript" src="static/bootstrap-ie11/js/bootstrap.bundle.min.js"><\/script>' +
            '<script type="text/javascript" src="static/bootstrap-ie11/js/polyfill.min.js"><\/script>' +
            '<script type="text/javascript" src="static/bootstrap-ie11/js/ie11-custom-properties.js"><\/script>'
        );
    } else {
        let importScript = document.createElement('script');
        importScript.setAttribute('src', 'static/bootstrap/js/bootstrap.bundle.min.js');
        document.head.appendChild(importScript);
    }
}

main()