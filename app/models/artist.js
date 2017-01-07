// app/models/artist.js
// load the things we need
var mongoose = require('mongoose');
var bcrypt   = require('bcrypt-nodejs');

// define the schema for our artist model
var artistSchema = mongoose.Schema({
    timeStamp : {type: Date, default: Date.now},

    numberOfUsers : {type: Date, default: 0, min: 0},

    name: String,

    spotifyId: String,

    soundcloudId: String
});

// create the model for artists and expose it to our app
module.exports = mongoose.model('Artist', artistSchema);