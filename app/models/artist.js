// app/models/artist.js
// load the things we need
var mongoose = require('mongoose');
var bcrypt   = require('bcrypt-nodejs');

// define the schema for our artist model
var artistSchema = mongoose.Schema({
    artist            : {
        id        : mongoose.Schema.Types.ObjectId,

        timeStamp : {type: Date, default: Date.now},

        numberOfUsers : {type: Number, default: 0, min: 0},

        name: String
    }
});

// create the model for artists and expose it to our app
module.exports = mongoose.model('Artist', artistSchema);