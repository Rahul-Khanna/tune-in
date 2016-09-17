// app/models/notification.js
// load the things we need
var mongoose = require('mongoose');
var bcrypt   = require('bcrypt-nodejs');

// define the schema for our notification model
var notificationSchema = mongoose.Schema({

    notification            : {
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

        songName: String,

        timeStamp: {type: Date},
    }
});

// create the model for notifications and expose it to our app
module.exports = mongoose.model('Notification', notificationSchema);