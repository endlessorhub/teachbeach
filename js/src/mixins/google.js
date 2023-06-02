

export const initGoogleSDK = () => {
  return new Promise((resolve) => {
  (function(d, s, id) {
      var js,
      fjs = d.getElementsByTagName(s)[0];
      js = d.createElement(s);
      js.id = id;
      js.src = "https://accounts.google.com/gsi/client";
      fjs.parentNode.insertBefore(js, fjs);
    })(document, "script");
  
  })
};

export const GoogleClientId = () => { 
  return process.env.GOOGLE_CLIENT_ID;
}