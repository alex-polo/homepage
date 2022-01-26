const currentLocation = window.location;
const endpointMemoryWidgets = currentLocation.href + 'memory-widgets';
const widgetsСontainer = document.getElementById('widgetsContainer');
const searchField = document.getElementById('searchField');
const memoryWidgetModalTitle = document.getElementById('memoryWidgetModalTitle');
const memoryWidgetModalContent = document.getElementById('memoryWidgetModalContent');


function showDangerMessageForPage() {
    let pElement = document.createElement('p');
    pElement.textContent = 'An unexpected error occurred on the page. Please contact your administrator.';
    pElement.className = "danger-message-page text-center";
    cleanHtmlCardsContainer();
    widgetsСontainer.append(pElement);
}

function synceWithServer(url, callback) {
    let xmlHttp = new XMLHttpRequest();

    xmlHttp.open("GET", url, false);
    xmlHttp.setRequestHeader("Pragma", "no-cache");
    xmlHttp.send();

    if (xmlHttp.status == 200) {
        let json = JSON.parse(xmlHttp.responseText);
        callback(json);
    } else {
        console.log('Server return code: ' + xmlHttp.status);
        showDangerMessageForPage('Failed to get data from server. Contact your administrator');
    }
}

function cleanHtmlCardsContainer() {
    widgetsСontainer.innerHTML = '';
}

function showMemoryWidgetModal(memoryWidget) {
    let memoryWidgetModal = new bootstrap.Modal(document.getElementById('memoryWidgetModal'));
    let endpointUrlMemoryWidgets = endpointMemoryWidgets + '/' + memoryWidget.id;
    console.log(endpointUrlMemoryWidgets)

    synceWithServer(endpointUrlMemoryWidgets, function(serverResponse) {
        success = serverResponse['success'];
        if (success) {
            value = serverResponse['value'];
            memoryWidgetModalTitle.textContent = value.name;
            memoryWidgetModalContent.textContent = value.content;
            memoryWidgetModal.show();
        } else {
            console.log('Failed to get content for memory widget');
            showDangerMessageForPage();
        }
    })
}


function createHtmlWidget(widget) {
    let divColumn = document.createElement('div');
    let divCard = document.createElement('div');
    let divCardBody = document.createElement('div');
    let divCardFooter = document.createElement('div');
    let h5Header = document.createElement('h5');
    let aTag = document.createElement('a');
    let spanTag = document.createElement('span')

    divCard.className = "card widget ";
    divColumn.className = "col-sm-6 col-md-4 col-xxl-3";
    divCardBody.className = "card-body widget-body text-center";
    divCardFooter.className = "card-footer widget-footer";
    h5Header.className = "card-title";
    aTag.className = "block-link";

    h5Header.textContent = widget.name;

    if (widget.type == 'link_widget') {
        aTag.href = widget.url;
        aTag.target = '_blank';
        spanTag.textContent = '';
    } else if (widget.type == 'memory_widget') {
        aTag.onclick = function() {
            showMemoryWidgetModal(widget);
        }
        spanTag.textContent = 'Памятка';
    } else {
        console.log('Attribute widget.type has an unknown value');
        showDangerMessageForPage();
    }

    divCardBody.append(h5Header);
    divCardFooter.append(spanTag);
    divCard.append(aTag);
    divCard.append(divCardBody);
    divCard.append(divCardFooter);
    divColumn.append(divCard);
    return divColumn;
}


function fillingWidgetsContainer(elementsArray) {
    for (let index = 0; index < elementsArray.length; index++) {
        group = elementsArray[index]
        nameGroup = String(Object.keys(group))
        massiveCards = group[nameGroup]

        let h5GroupName = document.createElement('h5')
        let divGroupWidgets = document.createElement('div')
        let divGroup = document.createElement('div')

        h5GroupName.textContent = nameGroup

        h5GroupName.className = 'text-center mt-5'
        divGroup.className = 'row align-items-center widget-group'
        divGroupWidgets.className = 'row g-4 mb-5'


        for (let innerIndex = 0; innerIndex < massiveCards.length; innerIndex++) {
            widgetFromServer = massiveCards[innerIndex]
            htmlWidget = createHtmlWidget(widgetFromServer)
            divGroupWidgets.append(htmlWidget)
        }

        divGroup.append(h5GroupName)
        divGroup.append(divGroupWidgets)
        widgetsСontainer.append(divGroup)
    }
}

function handlerResponseWidgets(serverResponse) {
    success = serverResponse['success']
    listWidgets = serverResponse['list_widgets']
    if (success) {
        fillingWidgetsContainer(listWidgets)
    } else {
        showDangerMessageForPage()
        console.log('Attribute widget.type has an unknown value')
    }
}

function searchWidgets(url, handlerCallback) {
    return function() {
        try {
            showSpinner()
            cleanHtmlCardsContainer()

            if (searchField.value.length > 0) {
                endpointUrl = new URL(url);
                endpointUrl.searchParams.set('search', searchField.value);
            } else
                endpointUrl = new URL(url);

            synceWithServer(endpointUrl, handlerCallback)
        } catch (error) {
            console.log(error)
            showDangerMessageForPage()
        } finally {
            hideSpinner()
        }
    }
}

function addEventsSearchWidgets(func) {
    searchField.onpaste = function() {
        func()
    }
    searchField.oninput = function() {
        func()
    }
}

function main() {
    // let urlWidgets = NaN

    if (namePage == 'shared_page') {
        urlWidgets = currentLocation.href + 'home/shared-widgets'
    } else if (namePage == 'private_page')
        urlWidgets = currentLocation.href + 'widgets'

    if (urlWidgets.length != NaN) {
        if (widgetsСontainer != null && searchField != null && urlWidgets != NaN) {
            const searchWidgetsFunction = searchWidgets(urlWidgets, handlerResponseWidgets)
            searchWidgetsFunction()
            addEventsSearchWidgets(searchWidgetsFunction)
        } else {
            showDangerMessageForPage()
            console.log('MAIN. Oops, an unexpected error occured ')
        }
    }
}


if (window.addEventListener) // W3C standard
    window.addEventListener('load', main, false)
else if (window.attachEvent) // Microsoft
    window.attachEvent('onload', main)


// function synceWithServerFunction(url, callback, container) {
//     fetch(url)
//         .then(response => response.json())
//         .then(server_response => callback(server_response, container));
// }


// function get_synce_server_function(url, callback, container) {
//     if (isInternetExplorer()) {
//         return ie_synce_from_server_function(url, callback, container)
//     } else {
//         return synce_from_server_function(url, callback, container)
//     }
// }