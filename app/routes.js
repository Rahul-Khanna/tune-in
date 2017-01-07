// app/routes.js
module.exports = function(app, passport) {

    // =====================================
    // HOME PAGE (with login links) ========
    // =====================================
    app.get('/', function(req, res) {
        res.render('index.ejs'); // load the index.ejs file
    });

    // =====================================
    // LOGIN ===============================
    // =====================================
    // show the login form
    app.get('/login', function(req, res) {

        // render the page and pass in any flash data if it exists
        res.render('login.ejs', { message: req.flash('loginMessage') }); 
    });

    // process the login form
    // app.post('/login', do all our passport stuff here);

    // =====================================
    // SIGNUP ==============================
    // =====================================
    // show the signup form
    app.get('/signup', function(req, res) {

        // render the page and pass in any flash data if it exists
        res.render('signup.ejs', { message: req.flash('signupMessage') });
    });

    // process the signup form
    app.post('/signup', passport.authenticate('local-signup', {
        successRedirect : '/profile', // redirect to the secure profile section
        failureRedirect : '/signup', // redirect back to the signup page if there is an error
        failureFlash : true // allow flash messages
    }));


    // =====================================
    // PROFILE SECTION =====================
    // =====================================
    // we will want this protected so you have to be logged in to visit
    // we will use route middleware to verify this (the isLoggedIn function)
    app.get('/profile', isLoggedIn, function(req, res) {
        res.render('profile.ejs', {
            user : req.user // get the user out of session and pass to template
        });
    });

    app.get('/auth/spotify',
      passport.authenticate('spotify', {scope: ['user-read-email', 'user-read-private', 'user-top-read'], showDialog: true}),
      function(req, res){
    // The request will be redirected to spotify for authentication, so this
    // function will not be called.
    });

    app.get('/auth/soundcloud',
      passport.authenticate('soundcloud'),
      function(req, res){
        // The request will be redirected to SoundCloud for authentication, so this
        // function will not be called.
      });

    // GET /auth/soundcloud/callback
    //   Use passport.authenticate() as route middleware to authenticate the
    //   request.  If authentication fails, the user will be redirected back to the
    //   login page.  Otherwise, the primary route function function will be called,
    //   which, in this example, will redirect the user to the home page.
    app.get('/auth/soundcloud/callback', 
      passport.authenticate('soundcloud', { failureRedirect: '/login' }),
      function(req, res) {
        res.redirect('/profile');
    });

    // GET /auth/spotify/callback
    //   Use passport.authenticate() as route middleware to authenticate the
    //   request. If authentication fails, the user will be redirected back to the
    //   login page. Otherwise, the primary route function function will be called,
    //   which, in this example, will redirect the user to the home page.
    app.get('/callback',
    passport.authenticate('spotify', { failureRedirect: '/login' }),
      function(req, res) {

    console.log(req.user.spotifyInfo.token, 'req spotify token');

    // console.log(req.user ,'user');
    // console.log(req.query.code, 'code')
    // // console.log(res);

    var client_id = '6806905d214241afa14aa1b8265a9274';
    var client_secret = 'd87f8fbfc9314a0d9bc2f958b6ee50d3';

    var spotifyApi = new SpotifyWebApi({
      clientId : client_id,
      clientSecret : client_secret,
      redirectUri : 'http://localhost:8888/callback'
    });


    res.redirect('/profile')
    });

    // =====================================
    // LOGOUT ==============================
    // =====================================
    app.get('/logout', function(req, res) {
        req.logout();
        res.redirect('/');
    });


};

// route middleware to make sure a user is logged in
function isLoggedIn(req, res, next) {

    // if user is authenticated in the session, carry on 
    if (req.isAuthenticated())
        return next();

    // if they aren't redirect them to the home page
    res.redirect('/');
}
