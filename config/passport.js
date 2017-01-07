// config/passport.js

// load all the things we need
var LocalStrategy   = require('passport-local').Strategy,
    SoundCloudStrategy = require('passport-soundcloud').Strategy;
    SpotifyStrategy = require('passport-spotify').Strategy;
    mongoose = require('mongoose');
    SpotifyWebApi = require('spotify-web-api-node');

var userSchema = mongoose.Schema({
    email: String,
    spotifyInfo: {
        token       : String,
        refresh     : String,
        id          : String,
        userName    : String,
        active      : Boolean,
        region      : String
    },
    soundCloudInfo: {
        token       : String,
        refresh     : String,
        id          : String,
        userName    : String,
        active      : Boolean
    }, 
    
    percOfTopArtists: { type: Number, min: 0, max: 100, default: 100},

    possibleArtists : [String],

    following: [String],

    newNotifications: [mongoose.Schema.Types.ObjectId],

    saveSongs: [mongoose.Schema.Types.ObjectId],

    timeStamp: {type: Date, default: Date.now},

    lastLogin: {type: Date}
});

// define the schema for our artist model
var artistSchema = mongoose.Schema({

    timeStamp : {type: Date, default: Date.now},

    numberOfUsers : {type: Number, default: 0, min: 0},

    name: String,

    spotifyId: String,

    soundcloudId: String
});

// create the model for artists and expose it to our app
var Artist = mongoose.model('Artist', artistSchema);
var User = mongoose.model('User', userSchema);


// mongoose.connect('mongodb://localhost:27017/tune-in');

// expose this function to our app using module.exports
module.exports = function(passport) {

    //* ============ SPOTIFY AUTH ============= *//
var client_id = '6806905d214241afa14aa1b8265a9274';
var client_secret = 'd87f8fbfc9314a0d9bc2f958b6ee50d3';

//* ============ SOUNDCLOUD AUTH ============= *//
var SOUNDCLOUD_CLIENT_ID = "bec141287e6a2a78f03e036e0e5f4520"
var SOUNDCLOUD_CLIENT_SECRET = "c59bb14f01cfcf6415e3e7f66a370f29";

    // =========================================================================
    // passport session setup ==================================================
    // =========================================================================
    // required for persistent login sessions
    // passport needs ability to serialize and unserialize users out of session

    // used to serialize the user for the session
    // passport.serializeUser(function(user, done) {
    //     done(null, user.id);
    // });

    // // used to deserialize the user
    // passport.deserializeUser(function(id, done) {
    //     User.findById(id, function(err, user) {
    //         done(err, user);
    //     });
    // });

    passport.serializeUser(function(user, done) {
      done(null, user);
    });

    passport.deserializeUser(function(user, done) {
      done(null, user);
    });


// Use the SpotifyStrategy within Passport.
//   Strategies in Passport require a `verify` function, which accept
//   credentials (in this case, an accessToken, refreshToken, and spotify
//   profile), and invoke a callback with a user object.



passport.use(new SpotifyStrategy({
    clientID: client_id,
    clientSecret: client_secret,
    passReqToCallback : true,
    callbackURL: "http://localhost:8888/callback"
  },
  function(req, accessToken, refreshToken, profile, done) {


    process.nextTick(function() {

             User.findOne({ 'spotifyInfo.id' :  profile.id }, function(err, user) {
            // if there are any errors, return the error
            if (err)
                return done(err);

            // check to see if theres already a user with that email
            if (user) {
                console.log('logging in existing user');
                console.log(user.spotifyInfo.token);
                return done(null, user);

            } else {

                console.log(accessToken, 'this is the users access token')

                var spotifyApi = new SpotifyWebApi({
                  clientId : client_id,
                  clientSecret : client_secret,
                  redirectUri : 'http://localhost:8888/callback'
                });

                spotifyApi.setAccessToken(accessToken);


                var idArray = [];
                spotifyApi.getUsersTopArtists()
                    .then(function(data) {
                        topArtists = data.body.items.map(function(obj) {
                            var rArr = [];
                            var artistObject = {id: obj.id, name: obj.name};
                            rArr.push(artistObject)
                            return rArr
                        })
                        // console.log(data);

                        topArtists.forEach(function(value){
                            Artist.findOne({'spotifyId': value.name}, function(err) {
                                if (err) 
                                    return done(err);

                                // if (artist) {
                                //     console.log('already existing artist');
                                // }

                                else {
                                    console.log('hi hi', typeof(value[0].name), typeof(value[0].id));
                                    var newArtist = new Artist({
                                        timeStamp : Date.now(),
                                        numberOfUsers : 1,
                                        name: value[0].name,
                                        spotifyId: value[0].id,
                                        soundcloudId: 'a'
                                    });

                                    // save the Artist
                                    newArtist.save(function(err, artist) {
                                        if(err) {
                                            console.log(err);
                                        } else {
                                            console.log("THE ARTIST HAS BEEN SAVED");
                                            console.log(artist._id);
                                            idArray.push(artist._id);
                                            return;
                                        }
                                    });

                                }

                            })
                        })

                    })
                    .then(function(data) {
                        console.log(idArray,'id array part one')
                        idArray= ['58577440e63561e2c62b8a6e', '58577440e63561e2c62b8a6f', '58577440e63561e2c62b8a70'];
                        var newUser = new User({
                            spotifyInfo: {
                                token       : accessToken,
                                refresh     : refreshToken,
                                id          : profile.id,
                                email       : profile.email,
                                region      : profile.country
                            },
                            following : idArray,
                            possibleArtists : idArray
                        });
        
                        // save the user
                        newUser.save(function(err) {
                            if (err)
                                console.log(err, 'err on new user save');
                            console.log(idArray, "user info saved pt2");
                        });
                    })

            }

        });

    })
 
  }
));

};