/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-y19m-614.us', // the auth0 domain prefix
    audience: 'coffee_shop', // the audience set for the auth0 app
    clientId: 's7jUW3HxX4BjqtPSYM6NWMtNSNEJy6nr', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:8080/login-results', // the base url of the running ionic application. 
  }
};
