// app/models/song.js
// load the things we need
var mongoose = require('mongoose');
var bcrypt   = require('bcrypt-nodejs');

// define the schema for our song model
var songSchema = mongoose.Schema({

    song            : {
        id        : mongoose.Schema.Types.ObjectId,

        spotifydInfo  : {
           id: String,
           url: String,
        },

        soundcloudInfo  : {
           id: String,
           url: String,
        },

        artistId    :mongoose.Schema.Types.ObjectId,

        name: String,

        timeStamp: {type: Date},
    }
});

// create the model for songs and expose it to our app
module.exports = mongoose.model('Song', songSchema);