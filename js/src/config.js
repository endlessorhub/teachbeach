const hostReg = /(.*)\.collabsocial\.io/;
const match = window.location.hostname.match(hostReg);
const companySlugExceptions = ['www', 'dev'];

export default {
    google: {
        mapApiKey: process.env.GOOGLE_MAPS_API_KEY,
        CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
        CALENDAR_API_KEY: process.env.GOOGLE_CALENDAR_API_KEY,
    },
    companySlug: match && !companySlugExceptions.some(v => v === match[1]) ? match[1].split(".dev").shift() : null,
    baseUrl: process.env.BASE_WEB_URL,
}