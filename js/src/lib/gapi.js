let gapi;
let gapiLoaded = new Promise((res, rej) => {
    window.gapiLoaded.then(() => {
        gapi = window.gapi;
        res(true);
    }).catch(e => rej(e))
})

// Array of API discovery doc URLs for APIs used by the quickstart
const DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"];

// Authorization scopes required by the API; multiple scopes can be
// included, separated by spaces.
const SCOPES = "https://www.googleapis.com/auth/calendar.readonly";
import config from '@/config'

function init(onInited, onError) {
    handleClientLoad(initClient(onInited, onError))
}

function handleClientLoad(cb) {
    gapi.load('client:auth2', cb);
}

/**
*  Initializes the API client library and sets up sign-in state
*  listeners.
*/
const initClient = (handleInitedCB, handleErrorCB) => () => {
    gapi.client.init({
        apiKey: config.google.CALENDAR_API_KEY,
        clientId: config.google.CLIENT_ID,
        discoveryDocs: DISCOVERY_DOCS,
        scope: SCOPES
    }).then(function () {
        // Listen for sign-in state changes.
        const getUserEmail = () => (gapi.auth2.getAuthInstance().currentUser.get().getBasicProfile() && gapi.auth2.getAuthInstance().currentUser.get().getBasicProfile().getEmail())
        gapi.auth2.getAuthInstance().isSignedIn.listen(() => handleInitedCB(getUserEmail()));
        handleInitedCB(getUserEmail());
    }, handleErrorCB);
}

/**
*  Sign in the user upon button click.
*/
function handleAuth() {
    return gapi.auth2.getAuthInstance().signIn();
}

/**
*  Sign out the user upon button click.
*/
function handleSignout() {
    return gapi.auth2.getAuthInstance().signOut();
}

/**
* Print the summary and start datetime/date of the next ten events in
* the authorized user's calendar. If no events are found an
* appropriate message is printed.
*/
function listUpcomingEvents() {
    return gapi.client.calendar.events.list({
        'calendarId': 'primary',
        'timeMin': (new Date()).toISOString(),
        'showDeleted': false,
        'singleEvents': true,
        'maxResults': 100,
        'orderBy': 'startTime'
    }).then(function(response) {
        return response.result.items;
    });
}

export {
    gapiLoaded,
    init,
    handleAuth,
    handleSignout,
    listUpcomingEvents,
}